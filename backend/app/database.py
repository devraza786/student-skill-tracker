import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# We use a proxy class to host the supabase client lazily
class SupabaseClientProxy:
    def __init__(self):
        self._client = None

    @property
    def client(self) -> Client:
        if self._client is None:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise RuntimeError("SUPABASE_URL or SUPABASE_KEY missing in environment variables")
            self._client = create_client(url, key)
        return self._client

    # Delegate common methods to the internal client
    def table(self, table_name: str):
        return self.client.table(table_name)

supabase = SupabaseClientProxy()
