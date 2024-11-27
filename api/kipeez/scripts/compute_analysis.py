import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import asyncio
from datetime import datetime, timedelta
from kipeez.data_logic.metrics.analysis_logic import AnalysisLogic, AnalysisConfig
from kipeez.routes.dashboards import WidgetParameters

async def run_analysis_for_2024():
    analysis_logic = AnalysisLogic()
    organisation_id = "3459175b-bf94-4a3e-bcec-8a6d0e0ab323"

    analysis_requested = {
        "sales_analysis_downsell": AnalysisConfig(),
        "sales_analysis_upsell": AnalysisConfig(),
        "sales_analysis_churn": AnalysisConfig(),
        "sales_analysis_new": AnalysisConfig(),
        "sales_analysis_flop": AnalysisConfig(),
        "sales_analysis_top": AnalysisConfig()
    }

    for month in range(1, 13):
        start_period = datetime(2024, month, 1)
        end_period = datetime(2024, month, 28)
        params_override = WidgetParameters(
            start_period=start_period.strftime('%Y-%m'),
            end_period=end_period.strftime('%Y-%m'),
            start_reference_period=(start_period - timedelta(days=365)).strftime('%Y-%m'),
            end_reference_period=(end_period - timedelta(days=365)).strftime('%Y-%m'),
        )

        analysis = await analysis_logic.get_analysis(
            organisation_id=organisation_id,
            analysis_requested=analysis_requested,
            params_override=params_override
        )

        print(f"Analysis for {start_period.strftime('%B %Y')} DONE")

if __name__ == "__main__":
    asyncio.run(run_analysis_for_2024())
