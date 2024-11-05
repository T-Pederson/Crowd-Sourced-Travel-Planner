from __main__ import app, supabase
from flask import jsonify, request
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

@app.route("/create-account", methods=["POST"])
def create_account():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    confirm_password = request.json.get("confirm_password", None)

    # Validate user input
    inputErrors = []
    if len(username) < 4 or len(username) > 16:
      inputErrors.append("Username must be between 4 & 16 characters long")
    if not re.search(r"^[A-Za-z0-9]+$", username):
      inputErrors.append("Username must only contain letters and/or numbers (A-Z, a-z, 0-9)")
    if not re.search(r"[A-Z]+", password):
      inputErrors.append("Password must contain at least one uppercase letter (A-Z)")
    if not re.search(r"[a-z]+", password):
      inputErrors.append("Password must contain at least one lowercase letter (a-z)")
    if not re.search(r"\d+", password):
      inputErrors.append("Password must contain at least one number (0-9)")
    if not re.search(r"[~!@#$%^&*=+.?]+", password):
      inputErrors.append("Password must contain at least one special character ~!@#$%^&*=+.?")
    if len(password) < 8 or len(password) > 256:
      inputErrors.append("Password must be between 8 & 256 characters long")
    if password != confirm_password:
      inputErrors.append("Password and Confirm Password do not match")

    # If user input is invalid, send error response
    if len(inputErrors) > 0:
      return jsonify({"errors": inputErrors}), 400
    
    # If username is already taken, send error response
    response = supabase.table("Users").select('username').eq('username', username).execute()
    if response.data:
      return jsonify({"errors": ["Username taken"]}), 400
    
    # Hash user's password and store new user credentials in DB
    pw_hash = bcrypt.generate_password_hash(password)

    response = supabase.table("Users").insert({
      'username': username,
      'password': pw_hash.decode()
    }).execute()

    if response.data:
      return jsonify({"msg": "User created successfully"}), 200
    else:
      return jsonify({"errors": ["Failed to create user"]}), 400
