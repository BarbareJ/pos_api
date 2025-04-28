def test_create_product(client):
    unit_resp = client.post("/units", json={"name": "ცალი"})
    if unit_resp.status_code == 201:
        unit_id = unit_resp.json()["unit"]["id"]
    else:
        all_units = client.get("/units").json()["units"]
        unit_id = all_units[0]["id"]

    product_data = {
        "unit_id": unit_id,
        "name": "Apple",
        "barcode": "1234567890",
        "price": 520
    }
    resp = client.post("/products", json=product_data)
    assert resp.status_code in (201, 409)


def test_duplicate_barcode_product(client):
    unit_resp = client.post("/units", json={"name": "DuplicateCheckUnit"})
    if unit_resp.status_code == 201:
        real_unit_id = unit_resp.json()["unit"]["id"]
    else:
        all_units = client.get("/units").json()["units"]
        real_unit_id = all_units[-1]["id"]

    barcode = "9876543210"
    first_resp = client.post("/products", json={
        "unit_id": real_unit_id,
        "name": "DuplicateTestProd",
        "barcode": barcode,
        "price": 100
    })
    second_resp = client.post("/products", json={
        "unit_id": real_unit_id,
        "name": "DuplicateTestProd2",
        "barcode": barcode,
        "price": 200
    })
    assert second_resp.status_code == 409, (
        f"Expected 409 duplicate barcode, got {second_resp.status_code}"
    )
    err_json = second_resp.json()
    assert "error" in err_json
    assert "already exists" in err_json["error"]["message"]


def test_list_products(client):
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert "products" in data
    assert isinstance(data["products"], list)


def test_read_product(client):
    all_prods = client.get("/products").json()["products"]
    if not all_prods:
        test_create_product(client)
        all_prods = client.get("/products").json()["products"]

    product_id = all_prods[0]["id"]
    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "product" in data
    assert data["product"]["id"] == product_id


def test_read_non_existing_product(client):
    non_existing_id = "11111111-2222-3333-4444-555555555555"
    resp = client.get(f"/products/{non_existing_id}")
    assert resp.status_code == 404
    err_data = resp.json()
    assert "error" in err_data
    assert "does not exist" in err_data["error"]["message"]


def test_update_product_price(client):
    all_prods = client.get("/products").json()["products"]
    if not all_prods:
        test_create_product(client)
        all_prods = client.get("/products").json()["products"]

    product_id = all_prods[0]["id"]
    resp = client.patch(f"/products/{product_id}", json={"price": 999})
    assert resp.status_code == 200

    updated = client.get(f"/products/{product_id}").json()["product"]
    assert updated["price"] == 999



