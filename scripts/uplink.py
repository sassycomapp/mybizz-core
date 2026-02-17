import anvil.server
anvil.server.connect("server_FXF6ZEI2CGY5KUHG62BDYVET-TUYORZGLGKI2HE4F")
@anvil.server.callable
def test_uplink():
    return "Uplink connected successfully!"
anvil.server.wait_forever()