def test_sales_report(client):
    init_resp = client.get("/sales")
    assert init_resp.status_code == 200
    init_data = init_resp.json()
    assert "sales" in init_data
    init_revenue = init_data["sales"]["revenue"]
    init_receipts = init_data["sales"]["n_receipts"]

    products = client.get("/products").json()["products"]
    if not products:
        u_resp = client.post("/units", json={"name": "SalesUnit"})
        if u_resp.status_code == 201:
            uid = u_resp.json()["unit"]["id"]
        else:
            uid = client.get("/units").json()["units"][0]["id"]

        client.post("/products", json={
            "unit_id": uid,
            "name": "SalesProd",
            "barcode": "111222333",
            "price": 100
        })
        products = client.get("/products").json()["products"]
    product_id = products[-1]["id"]

    r_create = client.post("/receipts", json={})
    rid = r_create.json()["receipt"]["id"]
    client.post(f"/receipts/{rid}/products", json={"id": product_id, "quantity": 5})
    client.patch(f"/receipts/{rid}", json={"status": "closed"})

    final_resp = client.get("/sales")
    assert final_resp.status_code == 200
    final_data = final_resp.json()
    new_revenue = final_data["sales"]["revenue"]
    new_n_receipts = final_data["sales"]["n_receipts"]

    assert new_n_receipts == init_receipts + 1
    assert new_revenue == init_revenue + 500


