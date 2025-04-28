def test_create_receipt(client):
    resp = client.post("/receipts", json={})
    assert resp.status_code == 201
    data = resp.json()
    assert "receipt" in data
    receipt = data["receipt"]
    assert "id" in receipt
    assert receipt["status"] == "open"
    assert receipt["total"] == 0
    assert isinstance(receipt["products"], list) and len(receipt["products"]) == 0


def test_add_product_to_receipt(client):
    product_list = client.get("/products").json()["products"]
    if not product_list:
        client.post("/products", json={
            "unit_id": "",
            "name": "Temporary",
            "barcode": "temp-barcode",
            "price": 200
        })
        u_resp = client.post("/units", json={"name": "temp-unit"})
        if u_resp.status_code == 201:
            uid = u_resp.json()["unit"]["id"]
        else:
            uid = client.get("/units").json()["units"][0]["id"]
        client.post("/products", json={
            "unit_id": uid,
            "name": "Temporary",
            "barcode": "temp-barcode",
            "price": 200
        })
        product_list = client.get("/products").json()["products"]

    product_id = product_list[-1]["id"]

    create_r = client.post("/receipts", json={})
    r_id = create_r.json()["receipt"]["id"]

    add_resp = client.post(
        f"/receipts/{r_id}/products",
        json={"id": product_id, "quantity": 3}
    )
    assert add_resp.status_code == 201
    updated = add_resp.json()["receipt"]
    assert updated["total"] > 0
    assert len(updated["products"]) == 1
    item = updated["products"][0]
    assert item["id"] == product_id
    assert item["quantity"] == 3


def test_close_receipt(client):
    r_create = client.post("/receipts", json={})
    rid = r_create.json()["receipt"]["id"]
    close_resp = client.patch(f"/receipts/{rid}", json={"status": "closed"})
    assert close_resp.status_code == 200
    read_resp = client.get(f"/receipts/{rid}")
    assert read_resp.status_code == 200
    rec = read_resp.json()["receipt"]
    assert rec["status"] == "closed"


def test_read_receipt(client):
    r_create = client.post("/receipts", json={})
    assert r_create.status_code == 201
    rid = r_create.json()["receipt"]["id"]

    r_read = client.get(f"/receipts/{rid}")
    assert r_read.status_code == 200
    data = r_read.json()
    assert "receipt" in data
    rec = data["receipt"]
    for field in ["id", "status", "products", "total"]:
        assert field in rec

    non_existing_id = "11111111-2222-3333-4444-555555555555"
    r_404 = client.get(f"/receipts/{non_existing_id}")
    assert r_404.status_code == 404
    err_data = r_404.json()
    assert "error" in err_data
    assert "does not exist" in err_data["error"]["message"]


def test_cannot_add_product_to_closed_receipt(client):
    r_create = client.post("/receipts", json={})
    rid = r_create.json()["receipt"]["id"]
    client.patch(f"/receipts/{rid}", json={"status": "closed"})

    add_resp = client.post(
        f"/receipts/{rid}/products",
        json={"id": "some-product-id", "quantity": 1}
    )
    assert add_resp.status_code == 403


def test_delete_open_receipt(client):
    r_create = client.post("/receipts", json={})
    rid = r_create.json()["receipt"]["id"]

    d_resp = client.delete(f"/receipts/{rid}")
    assert d_resp.status_code == 200

    check = client.get(f"/receipts/{rid}")
    assert check.status_code == 404


def test_delete_closed_receipt(client):
    r_create = client.post("/receipts", json={})
    rid = r_create.json()["receipt"]["id"]
    client.patch(f"/receipts/{rid}", json={"status": "closed"})

    d_resp = client.delete(f"/receipts/{rid}")
    assert d_resp.status_code == 403

