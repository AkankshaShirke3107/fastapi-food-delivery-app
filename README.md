# 🍕 FastAPI Food Delivery App (QuickBite API)

## 🚀 Project Overview
The **QuickBite Food Delivery API** is a backend system built using FastAPI as part of an internship project.  
It simulates a real-world food delivery platform where users can browse menu items, add items to cart, place orders, and perform advanced operations like search, sorting, and pagination.

This project demonstrates strong backend development skills including REST API design, data validation, and workflow implementation.

---

## 🎯 Objectives
- Build a complete FastAPI backend system
- Implement real-world API workflows
- Apply concepts from Day 1 to Day 6 of FastAPI training
- Design clean and scalable API structure

---

## 🛠️ Tech Stack
- **Backend Framework:** FastAPI
- **Language:** Python 3
- **Validation:** Pydantic
- **Server:** Uvicorn
- **API Testing:** Swagger UI

---

## 📂 Project Structure


---

## ⚙️ Features Implemented

### ✅ Day 1 – GET APIs
- Home route (`/`)
- Get all menu items (`/menu`)
- Get item by ID (`/menu/{id}`)
- Menu summary (`/menu/summary`)
- Get all orders (`/orders`)

---

### ✅ Day 2 – POST APIs + Pydantic
- Create orders using request body
- Input validation using:
  - `min_length`
  - `gt`, `le`
- Error handling using HTTPException

---

### ✅ Day 3 – Helper Functions & Filtering
- `find_item()` → Find item by ID
- `calculate_total()` → Calculate order cost
- Filtering using query parameters:
  - category
  - price
  - availability

---

### ✅ Day 4 – CRUD Operations
- **POST** `/menu` → Add new item
- **PUT** `/menu/{id}` → Update item
- **DELETE** `/menu/{id}` → Delete item

Handled:
- 201 Created
- 404 Not Found
- Duplicate validation

---

### ✅ Day 5 – Cart & Checkout Workflow
Multi-step process:
1. Add item to cart
2. View cart
3. Remove item from cart
4. Checkout and create order

---

### ✅ Day 6 – Advanced APIs
- 🔍 Search (`/menu/search`)
- 🔄 Sorting (`/menu/sort`)
- 📄 Pagination (`/menu/page`)
- 🧠 Combined Browse (`/menu/browse`)
