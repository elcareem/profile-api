# Mini Profile Service – FastAPI + JWT + SQLAlchemy + Image Upload

## Overview
Build a small backend API using FastAPI, JWT authentication, SQLAlchemy ORM, and image upload handling.

The goal is to create a user profile system where users can register, log in, update their profile, and upload a profile picture. Protected routes must require a valid JWT.
You must also **containerize the project using Docker**.
---

## Requirements

### 1. Register User (Public)
**POST** `/register`

**Request Body**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "12345"
}
```
## Expected Behavior
- Hash password
- Save user in database
- Return user ID and a success message

## 2. Login User (Public)
POST /login
Request Body
```
{
  "email": "john@example.com",
  "password": "12345"
}
```

## Expected Behavior

- Validate email + password

- Generate a JWT token containing:

    - user_id
 
    - expiration time

## Response
```
{
  "access_token": "<jwt-token>"
}
```

## 3. Get Current User Profile (Protected)

GET /me

## Authorization Header
```
Authorization: Bearer <token>
```

## Expected Behavior

- Validate JWT
- Decode token → extract user_id
- Return user profile

## Response Example
```
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "image_url": "http://localhost:8000/static/profile/1.jpg"
}
```
## 4. Upload Profile Image (Protected)

# POST /me/upload-image

## Form Data

- image: file

# Expected Behavior

-Validate JWT

-Save file to:

static/profile/<user_id>.jpg

```
Update image_url in database

Response

{
  "message": "Upload successful",
  "image_url": "http://localhost:8000/static/profile/1.jpg"
}
```
### Update image_url in database

### Response
```
{
  "message": "Upload successful",
  "image_url": "http://localhost:8000/static/profile/1.jpg"
}
```

# 5. Update Profile Information (Protected)

## PUT /me
```
Request Body Example

{
  "name": "New Name"
}
```

### Expected Behavior

- Validate JWT
- Update user details in DB
- Return a success message
