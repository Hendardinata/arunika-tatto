# Refactor `frontend/templates/admin/dashboard.html` Menjadi Modular

Lakukan refactoring pada file:

```text
templates/
└── admin/
    └── dashboard.html
```

Saat ini seluruh Dashboard Admin berada di dalam satu file `dashboard.html`. Saya ingin file ini dipecah menjadi beberapa template berdasarkan **fitur/menu** agar lebih mudah dikelola, dikembangkan, dan di-maintain.

## Menu yang Saat Ini Ada

Dashboard Admin memiliki menu sebagai berikut:

### Dashboard

* Overview
* Bookings
* Payments

### Konten Studio

* Artists
* Services
* Gallery
* Customers

### Sistem

* Settings

Selain itu terdapat:

* Logo / Brand
* Sidebar
* Header / Topbar
* Tombol "Lihat Website"
* Logout

---

## Struktur yang Diinginkan

Contoh struktur:

```text
templates/
└── admin/  
        ├── overview.html
        ├── bookings.html
        ├── payments.html
        ├── artists.html
        ├── services.html
        ├── gallery.html
        ├── customers.html
        └── settings.html
```

## Dashboard Utama

File `dashboard.html` sebaiknya hanya berisi:

* Base Layout
* Include Sidebar
* Include Header
* Area Content
* Include Footer
* Include Script

Contoh konsep:

```jinja
dashboard.html

{% include 'admin/partials/sidebar.html' %}

{% include 'admin/partials/header.html' %}

{% include current_page %}

{% include 'admin/partials/footer.html' %}

{% include 'admin/partials/scripts.html' %}
```

Sehingga seluruh isi fitur berada di file masing-masing.

---

## Aturan Refactoring

Jangan mengubah:

* UI
* UX
* CSS
* JavaScript
* API
* Route
* Function
* Event
* AJAX / Fetch
* Database

Refactoring ini hanya bertujuan memisahkan struktur file agar lebih modular.

---

## Hasil yang Diharapkan

Setelah refactoring:

* `dashboard.html` menjadi file utama yang ringan.
* Setiap menu memiliki file template sendiri.
* Sidebar terpisah.
* Header terpisah.
* Footer terpisah.
* Script dipisahkan apabila memungkinkan.
* Kode lebih bersih dan mudah dipahami.
* Mudah menambahkan fitur baru tanpa membuat satu file menjadi ribuan baris.
* Meminimalkan konflik saat pengembangan dan mempermudah maintenance.

Pastikan seluruh fungsi tetap berjalan 100% sama seperti sebelum refactoring (backward compatible), sehingga perubahan ini hanya meningkatkan struktur proyek tanpa mengubah perilaku aplikasi.
