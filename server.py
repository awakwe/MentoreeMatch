from Project import app
# app.run(debug=True, host="0.0.0.0")
app.run(debug=True)

app.secret_key = 'development'