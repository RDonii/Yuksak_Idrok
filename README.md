# Yuksak_Idrok
"Yuksak Idrok" nomli o'quv markazi veb sayti uchun REST API

## API ma'lumatnomasi

### Boshlang'ich ma'lumotlar
- URL: Hozirda ushbu app hech qayyerga host qilinmagan va faqat local run qilinilishi mumkin. Backend app standart `http://127.0.0.1:5000/` da host bo'ladi va frontend konfiguratsiyalariga ham shu URL proxy sifatida kiritilishi talab qilinadi.
- Authentication: ??????????????????????????????????????????????????????????????????????????. 

### Error Handling
Error lar JSON obyekt sifatida quyidagi formatda qaytadi:
```
{ 
    "error": 400,
    "message": "Xato bajarilgan amaliyot haqida ma`lumot"
}
```
Ushbu API bo'yicha Request lar muvaffaqiyatsizlikga uchraganida quyidagi 5 xatolikdan birini qaytaradi :
- 400: Bad Request
- 404: Resource Not Found
- 415: Unsupported Media Type
- 422: Unprocessable Entity 
- 500: Internal Server Error

### Endpoints 

#### GET /categories
- Umumiy:
    - Mavjud kategoriyalarning soni va barcha kategoriyalarni o'z ichiga ogan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": [
    {
      "id": 1,
      "name": "Til kurslari"
    },
    {
      "id": 2,
      "name": "Aniq fanlar"
    }
  ],
  "count": 2
}
```
#### POST /categories
- Umumiy:
    - Jo'natilgan 'name' dan foydalanib yangi kategoriya yaratadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - "name": "yangi kategoriya nomi" (required)
- Namuna: `curl -X POST -H 'Content-Type: application/json' -d '{"name": "IT sohalari"}' http://127.0.0.1:5000/categories`

```{
  "success": true
}
```

#### GET /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga teng id ga ega kategoriya nomini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories/3`

```{
  "name": "IT sohalari"
}
```

#### PATCH /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga teng id ga ega kategoriya nomini yuborilgan yangi nomga o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - "name": "kategoriya uchun yangi nom" (required)
- Namuna: `curl -X PATCH -H 'Content-Type: application/json' -d '{"name": "Abiturientlar uchun"}' http://127.0.0.1:5000/categories/2`

```{
  "success": true
}
```

#### DELETE /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga teng id ga ega kategoriyani bazadan o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/categories/2`

```{
  "success": true
}
```

#### GET /categories/{category_id}/courses
- Umumiy:
    - URL orqali yuborilgan id ga teng id ga ega kategoriyaga mansub kurslar soni va shu kurslarni o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories/4/courses`

```{
  "count": 3,
  "courses": [
    {
      "category_id": 4,
      "description": "100% natija",
      "id": 2,
      "img": "http://127.0.0.1:5000/display/0bb44c0c-0eae-475c-a1ac-4963109d56e9.jpg",
      "title": "Matematika"
    },
    {
      "category_id": 4,
      "description": "100% natijaga erishing.",
      "id": 4,
      "img": "http://127.0.0.1:5000/display/3a0e45ec-00c4-4d51-990f-7d977d238925.jpg",
      "title": "Fizika"
    },
    {
      "category_id": 4,
      "description": "100% natijaga erishing.",
      "id": 5,
      "img": "http://127.0.0.1:5000/display/8b44b0b2-2796-445c-9d64-c4103d92a120.jpg",
      "title": "Biologiya"
    }
  ]
}
```




#### GET /books
- General:
    - Returns a list of book objects, success value, and total number of books
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/books`

``` {
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```

#### POST /books
- General:
    - Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`
```
{
  "books": [
    {
      "author": "Neil Gaiman",
      "id": 24,
      "rating": 5,
      "title": "Neverwhere"
    }
  ],
  "created": 24,
  "success": true,
  "total_books": 17
}
```
#### DELETE /books/{book_id}
- General:
    - Deletes the book of the given ID if it exists. Returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
  "books": [
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    },
    {
      "author": "Kiese Laymon",
      "id": 12,
      "rating": 1,
      "title": "Heavy: An American Memoir"
    },
    {
      "author": "Emily Giffin",
      "id": 13,
      "rating": 4,
      "title": "All We Ever Wanted"
    },
    {
      "author": "Jose Andres",
      "id": 14,
      "rating": 4,
      "title": "We Fed an Island"
    },
    {
      "author": "Rachel Kushner",
      "id": 15,
      "rating": 1,
      "title": "The Mars Room"
    }
  ],
  "deleted": 16,
  "success": true,
  "total_books": 15
}
```
#### PATCH /books/{book_id}
- General:
    - If provided, updates the rating of the specified book. Returns the success value and id of the modified book. 
- `curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
```
{
  "id": 15,
  "success": true
}
```
