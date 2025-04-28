def test_create_unit(client):
    resp = client.post("/units", json={"name": "კგ"})
    assert resp.status_code == 201
    data = resp.json()
    assert "unit" in data
    unit_data = data["unit"]
    assert "id" in unit_data
    assert unit_data["name"] == "კგ"


def test_create_duplicate_unit(client):
    resp = client.post("/units", json={"name": "კგ"})
    assert resp.status_code == 409, f"Expected 409, got {resp.status_code}"
    error = resp.json()
    assert "error" in error
    assert "already exists" in error["error"]["message"]


def test_list_units(client):
    resp = client.get("/units")
    assert resp.status_code == 200
    data = resp.json()
    assert "units" in data
    units = data["units"]
    assert len(units) >= 1


def test_read_unit(client):
    all_units = client.get("/units").json()["units"]
    first_unit_id = all_units[0]["id"]
    read_resp = client.get(f"/units/{first_unit_id}")
    assert read_resp.status_code == 200
    data = read_resp.json()
    assert "unit" in data
    assert data["unit"]["id"] == first_unit_id


def test_read_non_existing_unit(client):
    non_existing_id = "11111111-2222-3333-4444-555555555555"

    resp = client.get(f"/units/{non_existing_id}")
    assert resp.status_code == 404
    err_data = resp.json()
    assert "error" in err_data
    assert "does not exist" in err_data["error"]["message"]
