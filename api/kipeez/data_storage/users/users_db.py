
from typing import List, Optional
from psycopg2 import Error
from kipeez.common.print_error import print_error
from kipeez.services.db.pool import pool
from kipeez.data_logic.users import User
from kipeez.data_storage.users.users_storage import UsersStorage
from kipeez.common.models.schema.setup import setup_users
from kipeez.data_storage.str_arr_to_uuids import str_arr_to_uuids
from kipeez.data_storage.array_agg_to_strings import array_agg_is_empty, array_agg_to_strings

class UsersDB(UsersStorage):
    @classmethod
    async def reset(cls):
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    cur.execute("DROP TABLE IF EXISTS users CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS user_logins CASCADE;")
                    conn.commit()
                    cur.execute(setup_users())
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in users_db:", error)
        finally:
            if conn:
                pool.putconn(conn)
    @classmethod
    async def get(cls, email: str = None, user_id: str = None) -> (User | None):
        found: List = None
        found_orgs = []
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:

                    fields = "id, email, first_name, last_name, disabled, hashed_password"
                    agg = "uo.organisation_id as organisation_id"
                    join = "LEFT JOIN user_organisations uo ON uo.user_id = u.id"
                    if email:
                        cur.execute(f"SELECT {fields}, {agg} FROM users u {join} WHERE u.email = %s", (email,))
                    else:
                        cur.execute(f"SELECT {fields}, {agg} FROM users u {join} WHERE u.id = %s", (user_id,))
            
                    results:List = cur.fetchall()

                    if len(results):
                        found = results[0]
                        row: List
                        for row in results: 
                            if row[6]:
                                found_orgs.append(row[6])

        except (Exception, Error) as error:
            print_error("Error in users_storage:", error)

        finally:
            if conn:
                pool.putconn(conn)
        
        if not found:
            return None
        return User(
            id= found[0],
            email= found[1],
            first_name= found[2],
            last_name= found[3],
            disabled= found[4],
            hashed_password= found[5],
            organisations_ids= found_orgs
            )
    @classmethod
    async def update(cls, user_id: str, columns: List[str], values: List[str])-> bool:
        if not columns or not values or len(columns) != len(values):
            return False
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    sets = []
                    for column, value in zip(columns, values):
                        sets.append(f"{column}={value}")
                    update_query = f"UPDATE users SET {','.join(sets)} WHERE id = UUID('{user_id}')"
                    cur.execute(update_query, )
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in users_storage:", error)
            return False

        finally:
            if conn:
                pool.putconn(conn)
                
        return True
    

    @classmethod
    async def track_login(cls, user_id: str) ->bool:
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    insert_query = """
                    INSERT INTO user_logins (user_id, login_at)
                    VALUES (%s, NOW())  -- using NOW() for current timestamp
                    """
                    cur.execute(insert_query, (user_id,))
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in users_storage:", error)
            return False

        finally:
            if conn:
                pool.putconn(conn)
                
        return True

    @classmethod
    async def find(self, ids: List[str]) -> List[User]:
        users = []
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    where = f"WHERE u.id = ANY({str_arr_to_uuids(ids)})" if ids else ""
                    wherewith = f"WHERE ul.user_id = ANY({str_arr_to_uuids(ids)})" if ids else ""
                    query = f"""
                    WITH RankedLogins AS (
                        SELECT 
                            ul.user_id, 
                            ul.login_at,
                            ROW_NUMBER() OVER (PARTITION BY ul.user_id ORDER BY ul.login_at DESC) AS rn
                        FROM 
                            user_logins ul
                        {wherewith}
                    )
                    SELECT u.id, email, first_name, last_name, disabled,
                    ARRAY_AGG(DISTINCT uo.organisation_id) AS organisation_id,
                    created_at,
                    ARRAY_AGG(ul.login_at ORDER BY ul.login_at DESC) AS last_10_logins
                    FROM users u
                    LEFT JOIN user_organisations uo ON uo.user_id = u.id
                    LEFT JOIN user_logins ul ON u.id = ul.user_id
                    {where}
                    GROUP BY u.id"""
                    cur.execute(query, )
                    conn.commit()
                    results = cur.fetchall()
                    row: List
                    for row in results: 
                        users.append(User(
                            id= row[0],
                            email= row[1],
                            first_name= row[2],
                            last_name= row[3],
                            disabled= row[4],
                            organisations_ids= array_agg_to_strings(row[5]),
                            created_at= row[6],
                            last_logins= row[7] if not array_agg_is_empty(row[7]) else []
                            ))
        except (Exception, Error) as error:
            print_error("Error in organisation_storage:", error)
            return []

        finally:
            if conn:
                pool.putconn(conn)
                
        return users
    
    @classmethod
    async def create(cls,
     email: str, hashed_password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> (bool):
        new_id = None
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    existing_user = await cls.get(email=email)
                    if existing_user:
                        print(f"User {email} already exists")
                        return None
                    insert_query = "INSERT INTO users (email, hashed_password, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id"
                    cur.execute(insert_query, (email, hashed_password, email if not first_name else first_name, email if not last_name else last_name))
                    conn.commit()
                    res: List = cur.fetchone()
                    new_id = res[0]

        except (Exception, Error) as error:
            print_error("Error in users_storage:", error)

        finally:
            if conn:
                pool.putconn(conn)
                
        return new_id
    
    @classmethod
    async def set_organisations(cls, user_id, organisations_ids) -> bool:
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM user_organisations WHERE user_id = UUID(%s)", (user_id,))
                    insert_query = f"INSERT INTO user_organisations (user_id, organisation_id) VALUES "
                    values = ','.join(f"(UUID('{user_id}'), UUID('{id}'))" for id in organisations_ids)
                    cur.execute(insert_query+values)
                    conn.commit()
                    return True
        except (Exception, Error) as error:
            print_error("Error in users_storage:", error)

        finally:
            if conn:
                pool.putconn(conn)
                
        return True
    

