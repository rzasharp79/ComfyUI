import types
import asyncio
from unittest.mock import patch

import pytest

@pytest.mark.asyncio
async def test_object_info_default_shape(aiohttp_client):
    # Create a dummy nodes module with a single node
    dummy_nodes = types.ModuleType('nodes')

    class DummyNode:
        @classmethod
        def INPUT_TYPES(cls):
            return {"required": {}}
        RETURN_TYPES = ()

    dummy_nodes.NODE_CLASS_MAPPINGS = {"DummyNode": DummyNode}
    dummy_nodes.NODE_DISPLAY_NAME_MAPPINGS = {}

    with patch.dict('sys.modules', {'nodes': dummy_nodes}):
        from server import PromptServer, DEFAULT_NODE_SHAPE
        from app.frontend_management import FrontendManager

        with patch.object(FrontendManager, 'init_frontend', return_value='webroot'):
            srv = PromptServer(asyncio.get_event_loop())
            client = await aiohttp_client(srv.app)
            resp = await client.get('/object_info/DummyNode')
            assert resp.status == 200
            data = await resp.json()
            assert data['DummyNode']['shape'] == DEFAULT_NODE_SHAPE
