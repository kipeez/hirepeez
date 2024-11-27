
from typing import List
from psycopg2 import Error
import psycopg2

from uuid import UUID
from kipeez.common.print_error import print_error
from kipeez.data_storage.str_arr_to_uuids import str_arr_to_uuids
from kipeez.data_logic.organisations import  Organisation
from kipeez.data_storage.organisations.organisations_storage import OrganisationsStorage
from kipeez.services.db.pool import pool
from kipeez.common.models.schema.setup import setup_organisations
from kipeez.data_storage.array_agg_to_strings import array_agg_to_strings
from kipeez.data_storage.is_valid_uuid import is_valid_uuid

class OrganisationsDB(OrganisationsStorage):
    @classmethod
    async def reset(cls):
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    cur.execute("DROP TABLE IF EXISTS user_organisations CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS organisation_invitations CASCADE;")
                    cur.execute("DROP TABLE IF EXISTS organisations CASCADE;")
                    conn.commit()
                    cur.execute(setup_organisations())
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)
        finally:
            if conn:
                pool.putconn(conn)

    @classmethod
    async def create(cls, name: str, slug: str, owner_id: str) -> str:
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    insert_query = f"INSERT INTO organisations (name, slug, owner_id) VALUES (%s, %s, UUID('{owner_id}')) RETURNING id"
                    cur.execute(insert_query, (name, slug, ))
                    conn.commit()
                    res:List = cur.fetchone()
                    new_id = res[0]
                    insert_query = f"INSERT INTO user_organisations (user_id, organisation_id) VALUES (UUID(%s), UUID(%s))"
                    cur.execute(insert_query, (owner_id, new_id, ))
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)
            return False

        finally:
            if conn:
                pool.putconn(conn)
                
        return new_id
    @classmethod
    async def update(cls, org_id: str, columns: List[str], values: List[str])-> bool:
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    sets = []
                    for column, value in zip(columns, values):
                        sets.append(f"{column}={value}")
                    update_query = f"UPDATE organisations SET {','.join(sets)} WHERE id = UUID('{org_id}')"
                    cur.execute(update_query, )
                    conn.commit()
        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)
            return False

        finally:
            if conn:
                pool.putconn(conn)
                
        return True
    @classmethod
    async def find(self, ids: List[str]) -> List[Organisation]:
        organisations = []
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    where = f"WHERE id = ANY({str_arr_to_uuids(ids)})" if ids else ""
                    query = f"""SELECT id, name, slug, owner_id, ARRAY_AGG(uo.user_id)
                        FROM organisations o LEFT JOIN user_organisations uo ON o.id = uo.organisation_id 
                        {where}
                        GROUP BY id"""
                    cur.execute(query, )
                    conn.commit()
                    results = cur.fetchall()
                    row: List
                    for row in results: 
                        organisations.append(Organisation(id=row[0], name=row[1], slug=row[2], owner_id=row[3], users_ids = array_agg_to_strings(row[4])))
        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)
            return False

        finally:
            if conn:
                pool.putconn(conn)
                
        return organisations
    @classmethod
    async def get(cls, id: str = None, slug: str = None) -> (Organisation | None):
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    where = f"WHERE id = UUID(%s)" if id else f"WHERE slug = %s"
                    query = f"""SELECT id, name, slug, owner_id, ARRAY_AGG(uo.user_id)
                        FROM organisations o LEFT JOIN user_organisations uo ON o.id = uo.organisation_id 
                        {where}
                        GROUP BY id"""
                    cur.execute(query, (id if id else slug,))
                    conn.commit()
                    results = cur.fetchall()
                    if len(results):
                        row = results[0]
                        return Organisation(id=row[0], name=row[1], slug=row[2], owner_id=row[3], users_ids = array_agg_to_strings(row[4]))

        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)

        finally:
            if conn:
                pool.putconn(conn)
        
        return None
    @classmethod
    async def add_user(cls, organisation_id, user_id) -> bool:
        conn = None
        try:
            conn = pool.getconn()
            with conn:
                with conn.cursor() as cur:
                    insert_query = f"""INSERT INTO user_organisations (user_id, organisation_id) VALUES (UUID(%s), UUID(%s))
                    ON CONFLICT (user_id, organisation_id) DO NOTHING"""
                    cur.execute(insert_query, (user_id, organisation_id))
                    conn.commit()
                    
                    return True
        except (Exception, Error) as error:
            print_error("Error in organisations_storage:", error)

        finally:
            if conn:
                pool.putconn(conn)
                
        return True