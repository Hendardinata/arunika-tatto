Berikut adalah **Implementation Plan** yang bisa dijadikan dokumen awal pengembangan aplikasi **Tattoo Studio Management System** menggunakan **Flask + MongoDB**. Saya buat dengan format yang biasa digunakan pada software development agar nantinya bisa langsung dijadikan acuan untuk PRD, SAD, maupun sprint.

---

# Implementation Plan

# Tattoo Studio Management System

### Version 1.0

---

# 1. Project Overview

## Nama Project

Tattoo Studio Management System

## Tujuan

Membangun sistem manajemen studio tattoo berbasis web yang memungkinkan pelanggan melakukan booking artist, memilih desain tattoo, melihat portofolio, melakukan konsultasi, serta mengirim permintaan pembayaran melalui WhatsApp.

Sistem ini ditujukan untuk meningkatkan efisiensi operasional studio sekaligus memberikan pengalaman pelanggan yang lebih profesional.

---

# 2. Technology Stack

## Backend

* Flask
* Flask Blueprint
* Flask Login
* Flask JWT (API)
* Flask-PyMongo

## Database

MongoDB

Collections:

```
users
artists
tattoos
bookings
payments
gallery
services
schedules
settings
messages
```

---

## Frontend

* HTML5
* Bootstrap 5
* Jinja2
* Javascript
* AJAX

---

## Deployment

Gunicorn

Nginx

MongoDB Atlas

Ubuntu Server

---

# 3. User Roles

## Admin

Hak akses

* Dashboard
* CRUD Artist
* CRUD Tattoo Service
* CRUD Gallery
* Booking Management
* Customer Management
* Payment Confirmation
* Schedule Management
* WhatsApp Configuration

---

## Tattoo Artist

Hak akses

* Melihat jadwal
* Mengubah status booking
* Upload hasil tattoo
* Melihat data customer

---

## Customer

Hak akses

* Registrasi
* Login
* Booking
* Upload referensi tattoo
* Pilih artist
* Chat WhatsApp
* Lihat histori booking

---

# 4. Main Features

## Authentication

* Login
* Register
* Forgot Password

---

## Artist Management

Admin dapat

Tambah artist

Edit artist

Hapus artist

Data artist

```
Nama

Foto

Instagram

Pengalaman

Keahlian

Status Aktif
```

---

## Tattoo Services

Contoh

```
Small Tattoo

Medium Tattoo

Large Tattoo

Cover Up

Custom Design

Touch Up
```

---

## Gallery

Menampilkan

Before

After

Kategori

Artist

Deskripsi

---

## Booking

Customer memilih

Tanggal

Jam

Artist

Jenis Tattoo

Referensi

Catatan

---

Booking Flow

```
Customer

↓

Pilih Artist

↓

Pilih Jadwal

↓

Isi Form

↓

Booking

↓

Pending

↓

Admin Review

↓

Approved

↓

Pembayaran

↓

Confirmed

↓

Tattoo Session

↓

Completed
```

---

## Schedule Management

Artist memiliki kalender

```
08.00

10.00

13.00

15.00

17.00
```

Admin dapat

Block tanggal

Libur

Reschedule

---

## Portfolio

Setiap artist memiliki halaman

```
Nama

Foto

Instagram

Style

Gallery

Review
```

---

## Customer Dashboard

Menampilkan

Booking aktif

Riwayat

Invoice

Status pembayaran

---

# 5. WhatsApp Payment Flow

Karena pembayaran diarahkan ke WhatsApp.

Flow

```
Booking

↓

Generate Invoice

↓

Klik Tombol Bayar

↓

Redirect ke WhatsApp

↓

Customer mengirim pesan otomatis

↓

Admin membalas

↓

Transfer Manual

↓

Upload Bukti

↓

Admin Konfirmasi

↓

Booking Aktif
```

---

Contoh pesan otomatis

```
Halo Admin Tattoo Studio.

Saya ingin melakukan pembayaran booking.

Invoice :

INV-20260015

Nama :

Andi

Artist :

Kevin

Tanggal :

12 Juli 2026

Total :

Rp450.000

Mohon konfirmasi pembayaran saya.
```

URL

```
https://wa.me/6281234567890?text=Halo%20Admin...
```

---

# 6. Database Design

## users

```
_id

fullname

email

password

phone

role

created_at
```

---

## artists

```
_id

name

photo

instagram

experience

specialization

description

status
```

---

## services

```
_id

name

price

duration

description
```

---

## bookings

```
_id

booking_code

customer_id

artist_id

service_id

date

time

reference_image

notes

status

created_at
```

---

## payments

```
_id

booking_id

amount

payment_method

payment_status

proof_image

confirmed_by

confirmed_at
```

---

## gallery

```
_id

artist_id

title

image

category

created_at
```

---

# 7. Folder Structure

```
project/

app/

auth/

booking/

artist/

gallery/

payment/

dashboard/

services/

customer/

models/

utils/

templates/

static/

uploads/

config.py

run.py
```

---

# 8. API Endpoint

Authentication

```
POST

/login

/register

/logout
```

Artist

```
GET /artists

POST /artists

PUT /artists/<id>

DELETE /artists/<id>
```

Booking

```
GET /bookings

POST /bookings

PUT /bookings/<id>

DELETE /bookings/<id>
```

Payment

```
POST /payment/send-whatsapp

POST /payment/upload-proof

GET /payment/history
```

Gallery

```
GET /gallery

POST /gallery

DELETE /gallery
```

---

# 9. Booking Status

```
Pending

↓

Approved

↓

Waiting Payment

↓

Payment Uploaded

↓

Confirmed

↓

Tattoo Process

↓

Completed

↓

Cancelled
```

---

# 10. Admin Dashboard

Menampilkan

```
Total Booking

Pendapatan

Artist Aktif

Customer

Booking Hari Ini

Waiting Payment

Tattoo Hari Ini

Completed
```

---

# 11. Notification

Customer

```
Booking berhasil

Booking disetujui

Menunggu pembayaran

Pembayaran diterima

Jadwal tattoo besok
```

Admin

```
Booking baru

Bukti pembayaran baru

Booking dibatalkan
```

---

# 12. Security

Password Hash

CSRF

Session Login

Role Based Access

Upload Validation

File Size Validation

Extension Validation

Rate Limiter

---

# 13. Future Development

* Midtrans Payment Gateway
* QRIS Payment
* WhatsApp API Integration
* Email Notification
* Reminder Otomatis
* Google Calendar Sync
* Digital Consent Form
* Membership & Loyalty Points
* Promo & Voucher
* Review dan Rating Artist
* Multi-Branch Support
* SaaS (Multi-Tenant) untuk banyak studio tattoo dengan domain dan branding masing-masing.

---

# 14. Development Roadmap

| Sprint   | Durasi   | Target                                                                |
| -------- | -------- | --------------------------------------------------------------------- |
| Sprint 1 | 1 minggu | Setup Flask, MongoDB, Authentication, Struktur Project                |
| Sprint 2 | 1 minggu | CRUD Artist, Service, Gallery                                         |
| Sprint 3 | 1 minggu | Booking System & Schedule Management                                  |
| Sprint 4 | 1 minggu | Dashboard Admin & Dashboard Customer                                  |
| Sprint 5 | 1 minggu | Integrasi WhatsApp Payment, Upload Bukti Pembayaran, Konfirmasi Admin |
| Sprint 6 | 1 minggu | Testing, Optimasi UI/UX, Deployment, Dokumentasi                      |

## Total Estimasi Waktu

Dengan satu developer full-time, estimasi pengembangan MVP adalah sekitar **6 minggu**. Setelah MVP stabil, pengembangan dapat dilanjutkan ke fitur lanjutan seperti notifikasi otomatis, integrasi payment gateway, dan arsitektur **SaaS multi-tenant** jika studio berkembang menjadi jaringan dengan banyak cabang atau ingin menawarkan platform kepada studio tattoo lain.
