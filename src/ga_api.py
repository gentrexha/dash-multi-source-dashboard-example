import os

from dotenv import load_dotenv

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.oauth2 import service_account
import pandas as pd


def generate_credentials():
    load_dotenv()
    json_account_info = {
        "type": "service_account",
        "project_id": "test-multi-sourc-1660741594169",
        "private_key_id": "3cb34bcb6da50c4ea2aad9d3ad4a4c140d76c6df",
        "private_key": os.environ["GOOGLE_APPLICATION_PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": "starting-account-sncw64yb4ov3@test-multi-sourc-1660741594169.iam.gserviceaccount.com",
        "client_id": "100924551939878499158",
        "auth_uri": "https://accounts.google.com/o/woauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/starting-account-sncw64yb4ov3%40test-multi-sourc-1660741594169.iam.gserviceaccount.com"
    }
    credentials = service_account.Credentials.from_service_account_info(json_account_info)
    return credentials


def run_request(property_id="YOUR-GA4-PROPERTY-ID") -> pd.DataFrame:
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    property_id = "316521862"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient(credentials=generate_credentials())

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2020-03-01", end_date="today")],
    )
    response = client.run_report(request)
    df = pd.DataFrame([{"date": row.dimension_values[0].value, "activeUsers": row.metric_values[0].value} for row in response.rows])
    df["date"] = pd.to_datetime(df["date"])
    df["activeUsers"] = pd.to_numeric(df["activeUsers"])
    return df


def main():
    run_request()


if __name__ == '__main__':
    main()
