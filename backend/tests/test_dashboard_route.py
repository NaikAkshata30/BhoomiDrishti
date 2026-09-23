from app import create_app


def test_dashboard_handles_missing_prediction_probabilities():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/api/dashboard')
        assert response.status_code == 200, response.get_data(as_text=True)
        payload = response.get_json()
        assert payload['success'] is True
        assert 'average_delay_probability' in payload
