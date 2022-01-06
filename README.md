# Yuksak_Idrok
"Yuksak Idrok" nomli o'quv markazi veb sayti uchun REST API

## API ma'lumatnomasi

### Boshlang'ich ma'lumotlar
- URL: Hozirda ushbu app hech qayyerga host qilinmagan va faqat local run qilinilishi mumkin. Backend app standart `http://127.0.0.1:5000/` da host bo'ladi va frontend konfiguratsiyalariga ham shu URL proxy sifatida kiritilishi talab qilinadi.
- Authentication: Sayt boshqaruvi uchun adminga imkoniyatlar yaratilgan bo'lib, barcha `PATCH`, `DELETE` va `POST`* metodlaridan faqatgina admin foydalana oladi. Yangi admin sifatida ro'yxatdan o'tish mumkin emas. (*`POST` metodi uchun yagona istisno - `/message` endpoint uchun token talab qilinmaydi.)


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
- 415: Unsupported Media Type*
- 422: Unprocessable Entity 
- 500: Internal Server Error

*ruxsat etilgan media kengaytmalari:
| Media turi | kengaytmasi |
| --- | --- |
| video | mp4, mov, wmv, avi |
| rasm | png, jpg, jpeg, gif |

### Endpoints 

#### GET /categories
- Umumiy:
    - Mavjud kategoriyalarning soni va barcha kategoriyalarni o'z ichiga ogan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories`

```
{
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

```
{
  "success": true
}
```

#### GET /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega kategoriya nomini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories/3`

```
{
  "name": "IT sohalari"
}
```

#### PATCH /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega kategoriya nomini yuborilgan yangi nomga o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - "name": "kategoriya uchun yangi nom" (required)
- Namuna: `curl -X PATCH -H 'Content-Type: application/json' -d '{"name": "Abiturientlar uchun"}' http://127.0.0.1:5000/categories/2`

```
{
  "success": true
}
```

#### DELETE /categories/{category_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega kategoriyani hamda shu kategoriyaga mansub guruh va kurslarni bazadan o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/categories/2`

```
{
  "success": true
}
```

#### GET /categories/{category_id}/courses
- Umumiy:
    - URL orqali yuborilgan id ga teng id ga ega kategoriyaga mansub kurslar soni va shu kurslarni o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/categories/4/courses`

```
{
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

#### GET /courses
- Umumiy:
    - Mavjud kurslar ro'yxatini olish uchun ishlatilinib, natija paginatsiyalanadi va ixtiyoriy ravishda sahifa qaramini hamda bir sahifadagi kurslar sonini tanlash mumkin.
    - Mavjud barcha kurslar sonini, kurslarni o'z ichiga olgan list obyektini, sahifa raqamini va shu sahifadagi kurslar sonini qaytaradi.
- Shartlar:
    - Argument sifatida "limit" va "page" qiymatlari uzatilishi mumkin
    - | Argument nomi | ta'rif | uzatilmaganida |
      | --- | --- | --- |
      | `page` | sahifa raqami | 1 |
      | `limit` | bir sahifada kurslar soni | 8 |
- Namuna: ` curl -sS 'http://127.0.0.1:5000/courses?page=2&limit=5' `

```
{
  "count": 10,
  "courses": [
    {
      "category_id": 3,
      "description": "Boshlang'ichlar uchun",
      "id": 6,
      "img": "http://127.0.0.1:5000/display/b497693e-133c-4487-ad04-1b0690c218ef.jpg",
      "title": "Node.js"
    },
    {
      "category_id": 3,
      "description": null,
      "id": 7,
      "img": "http://127.0.0.1:5000/display/0c9458ff-e0f4-430a-8221-f180684ba5c2.jpg",
      "title": "JavaScript"
    },
    {
      "category_id": 1,
      "description": null,
      "id": 8,
      "img": "http://127.0.0.1:5000/display/cf2bb0fd-fc61-47aa-a1ff-679fbf7fc2fe.jpg",
      "title": "Rus tili"
    },
    {
      "category_id": 1,
      "description": null,
      "id": 9,
      "img": "http://127.0.0.1:5000/display/52c9a6a9-b890-47b4-ba16-fa8082997ced.jpg",
      "title": "Ispan tili"
    },
    {
      "category_id": 3,
      "description": null,
      "id": 10,
      "img": "http://127.0.0.1:5000/display/eac42e38-0785-4c4a-82fc-40b63d08d516.jpg",
      "title": "HTML/CSS"
    }
  ],
  "limit": 5,
  "page": 2
}
```

#### POST /courses
- Umumiy:
    - Yangi kurs yaratadi. Ega kategoriya nomini yuborilgan yangi nomga o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `category` | `text` | kategoriya nomi. Mavjud kategoriyalardan biri tanlanadi | majburiy |
      | `title` | `text` | kurs nomi. Mavjud kurs nomi kiritilganda error qaytaradi. | majburiy |
      | `description` | `text` | kurs haqida | ixtiyoriy |
      | `image` | `file` | kurs uchun rasm yuklanadi | ixtiyoriy |
- Namuna: `curl -X POST -F "category=it sohalari" -F "title=Node.js" -F "description=Boshlang'ichlar uchun" -F "image=@rasm.jpg" http://127.0.0.1:5000/courses`
```
{
  "success": true
}
```

#### GET /courses/{course_id}
- Umumiy;
    - URL orqali yuborilgan id ga ega kursni o'z ichiga olgan list obyektni qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/courses/5`
```
{
  "course": [
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

#### PATCH /courses/{course_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega kursning ma'lumotlarini uzatilgan ma'lumotlarga o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif |
      | --- | --- | --- |
      | `category` | `text` | kategoriya nomi. Mavjud kategoriyalardan biri tanlanadi |
      | `title` | `text` | kurs nomi. Mavjud kurs nomi kiritilganda error qaytaradi. |
      | `description` | `text` | kurs haqida |
      | `image` | `file` | kurs uchun rasm yuklanadi |
- Namuna: `curl -X PATCH -F 'title=Spain' -F 'image=@rasm.jpg' http://127.0.0.1:5000/courses/9`
```
{
  "seccess": true
}
```

#### DELETE /courses/{course_id}
- Umumiy: 
    - URL orqali yuborilgan id ga ega kursni hamda shu kursga mansub guruhlarni bazadan o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/courses/12`
```
{
  "success": true
}
```

#### GET /individuals
- Umumiy:
    - Mavjud barcha individual kurslarni o'z ichiga olgan list obyektini va shu kurslar umumiy sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/individuals`
```
{
  "count": 5,
  "individuals": [
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 5,
      "in_month": 3,
      "members": 2,
      "price": 400000,
      "start": "12:00",
      "teacher_id": 1
    },
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 1,
      "end": "16:00",
      "id": 6,
      "in_month": 12,
      "members": 1,
      "price": 800000,
      "start": "14:00",
      "teacher_id": 3
    },
    {
      "active": false,
      "course_id": 2,
      "days": "[Du, Se, pa, sha]",
      "duration": 2,
      "end": "10:00",
      "id": 7,
      "in_month": 20,
      "members": 2,
      "price": 600000,
      "start": "18:00",
      "teacher_id": 2
    },
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 4,
      "end": "12:00",
      "id": 8,
      "in_month": 24,
      "members": 1,
      "price": 1000000,
      "start": "9:00",
      "teacher_id": 4
    },
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 1,
      "end": "18:00",
      "id": 9,
      "in_month": 18,
      "members": 1,
      "price": 1300000,
      "start": "14:00",
      "teacher_id": 4
    }
  ]
}
```


#### GET courses/{course_id}/individuals
- Umumiy:
    - URL orqali yuborilgan id ga ega kursga tegishli barcha individual kurslarni o'z ichiga olgan list obyekt va ularning umumiy sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/courses/2/individuals`
```
{
  "count": 3,
  "individuals": [
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 5,
      "in_month": 3,
      "members": 2,
      "price": 400000,
      "start": "12:00",
      "teacher_id": 1
    },
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 1,
      "end": "16:00",
      "id": 6,
      "in_month": 12,
      "members": 1,
      "price": 800000,
      "start": "14:00",
      "teacher_id": 3
    },
    {
      "active": false,
      "course_id": 2,
      "days": "[Du, Se, pa, sha]",
      "duration": 2,
      "end": "10:00",
      "id": 7,
      "in_month": 20,
      "members": 2,
      "price": 600000,
      "start": "18:00",
      "teacher_id": 2
    }
  ]
}
```

#### POST courses/{course_id}/individuals
- Umumiy:
    - URL orqali yuborilgan id ga ega kursga tegishli yangi individual guruh yaratadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - | o'zgaruvchi nomi | o'zgaruvchi turi | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `teacher_id` | `integer` | mas'ul o'qituvchiga tegishli id | majburiy |
      | `members` | `integer` | o'quvchilar soni | ixtiyoriy, default = 0 |
      | `price` | `integer` | bir oylik to'lov | majburiy |
      | `start` | `text` | dars boshlanish vaqti, masalan: `14:30` | ixtiyoriy |
      | `end` | `text` | dars tugash vaqti, masalan: `18:00` | ixtiyoriy |
      | `duration` | `integer` | kurs necha oy davom etishi | majburiy |
      | `days` | `text` | dars kunlari. Front uchun qulay ixtiyoriy ko'rinishda, masalan: `[DU, CHO, JU]` | ixtiyoriy |
      | `in_month` | `integer` | bir oydagi darslar soni | majburiy |
      | `active` | `boolean` | kursga qabul mavjudligi, masalar: `True` | ixtiyoriy, default=`False` |
- Namuna: `curl -X POST -H 'Content-Type: application/json' -d '{"teacher_id":1, "members":2, "price":400000, "start":"12:00", "end":"14:00", "duration":3, "days":"[Se, pa, sha]", "in_month":3, "active":true}' http://127.0.0.1:5000/courses/2/individuals`
```
{
  "success": true
}
```

#### GET /individuals/{individual_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega individual kursni o'z ichiga olgan list obyekt qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/individuals/7`
```
{
  "individual": [
    {
      "active": false,
      "course_id": 2,
      "days": "[Du, Se, pa, sha]",
      "duration": 2,
      "end": "10:00",
      "id": 7,
      "in_month": 20,
      "members": 2,
      "price": 600000,
      "start": "18:00",
      "teacher_id": 2
    }
  ]
}
```

#### PATCH /individuals/{individual_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega individual kursning ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - | o'zgaruvchi nomi | o'zgaruvchi turi | ta'rif |
      | --- | --- | --- |
      | `teacher_id` | `integer` | mas'ul o'qituvchiga tegishli id |
      | `members` | `integer` | o'quvchilar soni |
      | `price` | `integer` | bir oylik to'lov |
      | `start` | `text` | dars boshlanish vaqti, masalan: `14:30` |
      | `end` | `text` | dars tugash vaqti, masalan: `18:00` |
      | `duration` | `integer` | kurs necha oy davom etishi |
      | `days` | `text` | dars kunlari. Front uchun qulay ixtiyoriy ko'rinishda, masalan: `[DU, CHO, JU]` |
      | `in_month` | `integer` | bir oydagi darslar soni |
      | `active` | `boolean` | kursga qabul mavjudligi, masalar: `True` |
- Namuna: `curl -X PATCH -H 'Content-Type: application/json' -d '{"members":1, "price":700000, "active":true}' http://127.0.0.1:5000/individuals/7`
```
{
  "success": true
}
```

#### DELETE /individuals/{individual_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega individual kursni o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/individuals/10`
```
{
  "success": true
}
```

#### GET /groups
- Umumiy:
    - Mavjud barcha guruhlarni o'z ichiga olgan list obyektini va shu guruhlar umumiy sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/groups`
```
{
  "count": 5,
  "groups": [
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 1,
      "in_month": 3,
      "members": 12,
      "price": 300000,
      "start": "12:00",
      "teacher_id": 2
    },
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 2,
      "end": "18:00",
      "id": 2,
      "in_month": 22,
      "members": 15,
      "price": 500000,
      "start": "16:00",
      "teacher_id": 1
    },
    {
      "active": true,
      "course_id": 2,
      "days": "belgilanmagan",
      "duration": 5,
      "end": "19:00",
      "id": 3,
      "in_month": 15,
      "members": 8,
      "price": 450000,
      "start": "15:00",
      "teacher_id": 3
    },
    {
      "active": false,
      "course_id": 1,
      "days": "belgilanmagan",
      "duration": 2,
      "end": "17:00",
      "id": 4,
      "in_month": 24,
      "members": 22,
      "price": 350000,
      "start": "13:00",
      "teacher_id": 4
    },
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 5,
      "in_month": 3,
      "members": 7,
      "price": 300000,
      "start": "12:00",
      "teacher_id": 4
    }
  ]
}
```

#### GET courses/{course_id}/groups
- Umumiy:
    - URL orqali yuborilgan id ga ega kursga tegishli barcha guruhlarni o'z ichiga olgan list obyekt va ularning umumiy sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/courses/2/groups`
```
{
  "count": 3,
  "groups": [
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 1,
      "in_month": 3,
      "members": 12,
      "price": 300000,
      "start": "12:00",
      "teacher_id": 2
    },
    {
      "active": true,
      "course_id": 2,
      "days": "[Se, pa, sha]",
      "duration": 2,
      "end": "18:00",
      "id": 2,
      "in_month": 22,
      "members": 15,
      "price": 500000,
      "start": "16:00",
      "teacher_id": 1
    },
    {
      "active": true,
      "course_id": 2,
      "days": "belgilanmagan",
      "duration": 5,
      "end": "19:00",
      "id": 3,
      "in_month": 15,
      "members": 8,
      "price": 450000,
      "start": "15:00",
      "teacher_id": 3
    }
  ]
}
```

#### POST courses/{course_id}/groups
- Umumiy:
    - URL orqali yuborilgan id ga ega kursga tegishli yangi guruh yaratadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - | o'zgaruvchi nomi | o'zgaruvchi turi | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `teacher_id` | `integer` | mas'ul o'qituvchiga tegishli id | majburiy |
      | `members` | `integer` | o'quvchilar soni | ixtiyoriy, default = 0 |
      | `price` | `integer` | bir oylik to'lov | majburiy |
      | `start` | `text` | dars boshlanish vaqti, masalan: `14:30` | ixtiyoriy |
      | `end` | `text` | dars tugash vaqti, masalan: `18:00` | ixtiyoriy |
      | `duration` | `integer` | kurs necha oy davom etishi | majburiy |
      | `days` | `text` | dars kunlari. Front uchun qulay ixtiyoriy ko'rinishda, masalan: `[DU, CHO, JU]` | ixtiyoriy |
      | `in_month` | `integer` | bir oydagi darslar soni | majburiy |
      | `active` | `boolean` | kursga qabul mavjudligi, masalar: `True` | ixtiyoriy, default=`False` |
- Namuna: `curl -X POST -H 'Content-Type: application/json' -d '{"teacher_id":2, "members":12, "price":300000, "start":"12:00", "end":"14:00", "duration":3, "days":"[Se, pa, sha]", "in_month":3, "active":true}' http://127.0.0.1:5000/courses/2/groups`
```
{
  "success": true
}
```

#### GET /groups/{group_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega individual kursni o'z ichiga olgan list obyekt qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/groups/3`
```
{
  "group": {
    "active": true,
    "course_id": 2,
    "days": "belgilanmagan",
    "duration": 5,
    "end": "19:00",
    "id": 3,
    "in_month": 15,
    "members": 8,
    "price": 450000,
    "start": "15:00",
    "teacher_id": 3
  }
}
```

#### PATCH /groups/{group_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega guruhning ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: application/json
    - | o'zgaruvchi nomi | o'zgaruvchi turi | ta'rif |
      | --- | --- | --- |
      | `teacher_id` | `integer` | mas'ul o'qituvchiga tegishli id |
      | `members` | `integer` | o'quvchilar soni |
      | `price` | `integer` | bir oylik to'lov |
      | `start` | `text` | dars boshlanish vaqti, masalan: `14:30` |
      | `end` | `text` | dars tugash vaqti, masalan: `18:00` |
      | `duration` | `integer` | kurs necha oy davom etishi |
      | `days` | `text` | dars kunlari. Front uchun qulay ixtiyoriy ko'rinishda, masalan: `[DU, CHO, JU]` |
      | `in_month` | `integer` | bir oydagi darslar soni |
      | `active` | `boolean` | kursga qabul mavjudligi, masalar: `True` |
- Namuna: `curl -X PATCH -H 'Content-Type: application/json' -d '{"members":10, "price":350000}' http://127.0.0.1:5000/groups/3`
```
{
  "success": true
}
```

#### DELETE /groups/{group_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega guruhni o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/groups/6`
```
{
  "success": true
}
```

#### GET /teachers
- Umumiy:
    - Mavjud barcha o'qituvchilarni o'z ichiga olgan list obyekti va ularning umumiy sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/teachers`
```
{
  "count": 4,
  "teachers": [
    {
      "description": "juda kop fanlar nomzodi :)",
      "first_name": "Ali",
      "id": 1,
      "img": "http://127.0.0.1:5000/display/35d026d1-c4d8-4d66-b084-3c8b9a6b8491.jpg",
      "last_name": "Valiyev"
    },
    {
      "description": "",
      "first_name": "Shermat",
      "id": 2,
      "img": "http://127.0.0.1:5000/display/11554fb5-6af3-4fa0-b78f-c333e262578f.jpg",
      "last_name": "Eshmatov"
    },
    {
      "description": "Avstraliyalik",
      "first_name": "John",
      "id": 3,
      "img": "http://127.0.0.1:5000/display/87ae97be-dd19-4d86-bad9-2e44f0edb302.jpg",
      "last_name": "Smith"
    },
    {
      "description": "",
      "first_name": "Akbar",
      "id": 4,
      "img": "http://127.0.0.1:5000/display/5a068767-72df-4b5d-82b6-22fcf8ce3f32.jpg",
      "last_name": "Jakbarov"
    }
  ]
}
```

#### POST /teachers
- Umumiy: Yangi o'qituvchi qo'shadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `first_name` | `text` | o'qituvchi ismi | majburiy |
      | `last_name` | `text` | o'qituvchi familiyasi | ixtiyoriy |
      | `description` | `text` | o'qituvchi haqida | ixtiyoriy |
      | `image` | `file` | o'qituvchi rasmi | ixtiyoriy |
- Namuna: `curl -X POST -H 'Content-Type: multipart/form-data' -F 'first_name=Mr Bob' -F 'description=15 yillik tajriba va hokazolar' -F 'image=@rasm.jpg' http://127.0.0.1:5000/teachers`
```
{
  "success": true
}
```

#### GET /teachers/{teacher_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega o'qituvchini o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/teachers/4`
```
{
  "teacher": {
    "description": "",
    "first_name": "Akbar",
    "id": 4,
    "img": "http://127.0.0.1:5000/display/5a068767-72df-4b5d-82b6-22fcf8ce3f32.jpg",
    "last_name": "Jakbarov"
  }
}
```

#### PATCH /teachers/{teacher_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega o'qituvchining ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif |
      | --- | --- | --- | --- |
      | `first_name` | `text` | o'qituvchi ismi |
      | `last_name` | `text` | o'qituvchi familiyasi |
      | `description` | `text` | o'qituvchi haqida |
      | `image` | `file` | o'qituvchi rasmi |
- Namuna: `curl -X PATCH -H 'Content-Type: multipart/form-data' -F 'last_name=Johnson' http://127.0.0.1:5000/teachers/5`
```
{
  "success": true
}
```

#### DELETE /teachers/{teacher_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega o'qituvchini (agar unga bog'langan guruhlar mavjud bo'lmasa) bazadan o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuma: `curl -X DELETE http://127.0.0.1:5000/teachers/6`
```
{
  "success": true
}
```

#### GET /teachers/{teacher_id}/courses
- Umumiy:
    - URL orqali yuborilgan id ga ega o'qituvchiga tegishli barcha individual kurslarni va va ularning sonini, guruhiy kurslarni va ularning sonini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/teachers/4/courses`
```
{
  "count_groups": 2,
  "count_individuals": 2,
  "groups": [
    {
      "active": false,
      "course_id": 1,
      "days": "belgilanmagan",
      "duration": 2,
      "end": "17:00",
      "id": 4,
      "in_month": 24,
      "members": 22,
      "price": 350000,
      "start": "13:00",
      "teacher_id": 4
    },
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 3,
      "end": "14:00",
      "id": 5,
      "in_month": 3,
      "members": 7,
      "price": 300000,
      "start": "12:00",
      "teacher_id": 4
    }
  ],
  "individuals": [
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 4,
      "end": "12:00",
      "id": 8,
      "in_month": 24,
      "members": 1,
      "price": 1000000,
      "start": "9:00",
      "teacher_id": 4
    },
    {
      "active": true,
      "course_id": 1,
      "days": "[Se, pa, sha]",
      "duration": 1,
      "end": "18:00",
      "id": 9,
      "in_month": 18,
      "members": 1,
      "price": 1300000,
      "start": "14:00",
      "teacher_id": 4
    }
  ]
}
```

#### GET /teachers/{teacher_id}/certifications
- Umumiy:
    - URL orqali yuborilgan id ga ega o'qituvchiga tegishli barcha sertifikatlarni o'z ichiga olgan list obyekt va ularning sonini qaytaradi.
Namuna: `curl http://127.0.0.1:5000/teachers/4/certifications`
```
{
  "certifications": [
    {
      "credential": "link/to/confirm",
      "given_by": "WWC inc.",
      "id": 1,
      "img": "http://127.0.0.1:5000/display/813bd65d-70cb-4fb0-a43b-ae00e27e4c55.jpg",
      "teacher_id": 4,
      "title": "Data Guru"
    },
    {
      "credential": "",
      "given_by": "WWC inc.",
      "id": 2,
      "img": "http://127.0.0.1:5000/display/e6286182-8a29-4c37-aad5-6b02cb57b994.jpg",
      "teacher_id": 4,
      "title": "Full Stack Developer"
    }
  ],
  "count": 2
}
```

#### GET /certifications
- Umumiy:
    - Mavjud barcha sertifikatlarni* o'z ichiga olgan list obyektini qaytaradi.
    - Sertifikatlar - o'qituvchilarga tegishli bo'lib, yutuqlari, unvon yoki sovrinlari bo'lishi mumkin.
Namuna: `curl http://127.0.0.1:5000/certifications`
```
{
  "certifications": [
    {
      "credential": "link/to/confirm",
      "given_by": "WWC inc.",
      "id": 1,
      "img": "http://127.0.0.1:5000/display/813bd65d-70cb-4fb0-a43b-ae00e27e4c55.jpg",
      "teacher_id": 4,
      "title": "Data Guru"
    },
    {
      "credential": "",
      "given_by": "WWC inc.",
      "id": 2,
      "img": "http://127.0.0.1:5000/display/e6286182-8a29-4c37-aad5-6b02cb57b994.jpg",
      "teacher_id": 4,
      "title": "Full Stack Developer"
    },
    {
      "credential": "",
      "given_by": "",
      "id": 3,
      "img": "http://127.0.0.1:5000/display/ebfea31e-f5b2-4f9b-bd36-ef951218c306.jpg",
      "teacher_id": 2,
      "title": "Xalq Ta`lim A`lochisi"
    }
  ],
  "count": 3
}
```

#### POST /certifications
- Umumiy:
    - Yangi sertifikat qo'shadi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `teacher_id` | `integer` | sertifikat egasiga tegishli id | majburiy |
      | `title` | `text` | sertifikat nomi | majburiy |
      | `given_by` | `text` | kim tomonidan berilganligi | ixtiyoriy |
      | `credential` | `text` | tasdiqlovchi link | ixtiyoriy |
      | `image` | `file` | sertifikat rasmi | ixtiyoriy |
- Namuna: `curl -X POST -H 'Content-Type: multipart/form-data' -F 'teacher_id=4' -F 'title=Data Guru' -F 'given_by=WWC inc.' -F 'credential=link/to/confirm' -F 'image=@rasm.jpg' http://127.0.0.1:5000/certifications`
```
{
  "success": true
}
```

#### GET /certifications/{certification_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega sertifikatni o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/certifications/2`
```
{
  "certification": {
    "credential": "",
    "given_by": "WWC inc.",
    "id": 2,
    "img": "http://127.0.0.1:5000/display/e6286182-8a29-4c37-aad5-6b02cb57b994.jpg",
    "teacher_id": 4,
    "title": "Full Stack Developer"
  }
}
```

#### PATCH /certifications/{certification_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega sertifikat ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif |
      | --- | --- | --- |
      | `teacher_id` | `integer` | sertifikat egasiga tegishli id |
      | `title` | `text` | sertifikat nomi |
      | `given_by` | `text` | kim tomonidan berilganligi |
      | `credential` | `text` | tasdiqlovchi link |
      | `image` | `file` | sertifikat rasmi |
- Namuna: `curl -X PATCH -H 'Content-Type: multipart/form-data' -F 'credential=link/to/confirm' http://127.0.0.1:5000/certifications/2`
```
{
  "success": true
}
```

#### DELETE /certifications/{certification_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega sertifikatni o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/certifications/4`
```
{
  "success": true
}
```

#### GET /awards
- Umumiy:
    - Mavjud barcha yutuqlarni* o'z ichiga olgan list obyektini qaytaradi.
    - Yutuqlar - o'quv markaziga tegishli bo'lib, sovrinlari, muhofot yoki biror reytingda erishgan o'rni bo'lishi mumkin.
Namuna: `curl http://127.0.0.1:5000/awards`
```
{
  "awards": [
    {
      "credential": "link/to/confirm",
      "given_by": "WWC inc.",
      "given_year": "",
      "id": 1,
      "img": "http://127.0.0.1:5000/display/c9cf3305-ed2f-4f30-b945-a6df47453e50.jpg",
      "title": "Yil markazi"
    },
    {
      "credential": "link/to/news/about/this",
      "given_by": "XTV",
      "given_year": "",
      "id": 2,
      "img": "http://127.0.0.1:5000/display/48207aae-fa10-4e41-bc04-9cc085c048f5.jpg",
      "title": "in TOP5 of 2021"
    }
  ],
  "count": 2
}
```

#### POST /awards
- Umumiy: Yangi yutuq qo'shadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `title` | `text` | nomi | majburiy |
      | `given_by` | `text` | kim tomonidan berilganligi | ixtiyoriy |
      | `given_year` | `text` | qaysi yil berilganligi | ixtiyoriy |
      | `credential` | `text` | tasdiqlovchi link | ixtiyoriy |
      | `image` | `file` | rasmi | ixtiyoriy |
- Namuna: `curl -X POST -H 'Content-Type: multipart/form-data' -F 'title=Yil markazi' -F 'given_by=WWC inc.' -F 'credential=link/to/confirm' -F 'image=@rasm.jpg' http://127.0.0.1:5000/awards`
```
{
  "success": true
}
```

#### GET /awards/{award_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yutuqni o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/awards/2`
```
{
  "award": {
    "credential": "link/to/news/about/this", 
    "given_by": "XTV", 
    "given_year": "", 
    "id": 2, 
    "img": "http://127.0.0.1:5000/display/48207aae-fa10-4e41-bc04-9cc085c048f5.jpg", 
    "title": "in TOP5 of 2021"
  }
}
```

#### PATCH /awards/{award_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yutuq ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif |
      | --- | --- | --- |
      | `title` | `text` | nomi |
      | `given_by` | `text` | kim tomonidan berilganligi |
      | `given_year` | `text` | qaysi yil berilganligi |
      | `credential` | `text` | tasdiqlovchi link |
      | `image` | `file` | rasmi |
- Namuna: `curl -X PATCH -H 'Content-Type: multipart/form-data' -F 'given_year=2021' http://127.0.0.1:5000/awards/2`
```
{
  "success": true
}
```

#### DELETE /awards/{award_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yutuqni o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/awards/3`
```
{
  "success": true
}
```

#### GET /news
- Umumiy:
    - Mavjud barcha yangiliklarni o'z ichiga olgan list obyektini qaytaradi.
Namuna: `curl http://127.0.0.1:5000/news`
```
{
  "count": 3,
  "news": [
    {
      "id": 2,
      "img": "http://127.0.0.1:5000/display/2e5a5967-12b9-41ef-92db-194fc7a36cfd.jpg",
      "subtitle": "Kaatta matin bor bu yerda",
      "title": "Qabul boshlandi",
      "video": "http://127.0.0.1:5000/display/5da4d47c-292d-4139-b04f-57ee1529357c.mp4"
    },
    {
      "id": 3,
      "img": "http://127.0.0.1:5000/display/bd01153f-57e3-4ef0-87fb-0804bd1ebe9d.jpg",
      "subtitle": "Kaatta matin bor bu yerda",
      "title": "Ikkinchi yangilik",
      "video": "http://127.0.0.1:5000/display/fc8c7fbd-ab18-4ad8-844b-0bc6a0471bbb.mp4"
    },
    {
      "id": 4,
      "img": "http://127.0.0.1:5000/display/5edf8812-3f7c-41c1-914a-54ac830cfcb3.jpg",
      "subtitle": "Kaatta matin bor bu yerda",
      "title": "yana bir yangilik",
      "video": "http://127.0.0.1:5000/display/988b8d91-06c3-4b71-a63c-1ad58d47fec1.mp4"
    }
  ]
}
```

#### POST /news
- Umumiy: Yangi yangilik qo'shadi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif | shartligi |
      | --- | --- | --- | --- |
      | `title` | `text` |  sarlavha | majburiy |
      | `subtitle` | `text` | asosiy matin | majburiy |
      | `image` | `file` | rasm | ixtiyoriy |
      | `video` | `file` | video | ixtiyoriy |
- Namuna: `curl -X POST -H 'Content-Type: multipart/form-data' -F 'title=Qabul boshlandi' -F 'subtitle=Kaatta matin bor bu yerda' -F 'image=@rasm.jpg' -F 'video=@video.mp4' http://127.0.0.1:5000/news`
```
{
  "success": true
}
```


#### GET /news/{news_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yangilikni o'z ichiga olgan list obyektini qaytaradi.
- Namuna: `curl http://127.0.0.1:5000/news/2`
```
{
  "news": {
    "id": 2,
    "img": "http://127.0.0.1:5000/display/2e5a5967-12b9-41ef-92db-194fc7a36cfd.jpg",
    "subtitle": "Kaatta matin bor bu yerda",
    "title": "Qabul boshlandi",
    "video": "http://127.0.0.1:5000/display/5da4d47c-292d-4139-b04f-57ee1529357c.mp4"
  }
}
```


#### PATCH /news/{news_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yangilik ma'lumotlarini o'zgartiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Shartlar:
    - Content-Type: multipart/form-data
    - | `name` | `input type` | ta'rif |
      | --- | --- | --- |
      | `title` | `text` |  sarlavha |
      | `subtitle` | `text` | asosiy matin |
      | `image` | `file` | rasm |
      | `video` | `file` | video |
- Namuna: `curl -X PATCH -H 'Content-Type: multipart/form-data' -F 'title=yangi sarlavha' -F 'subtitle=yangilangan matin' http://127.0.0.1:5000/news/4`
```
{
  "success": true
}
```

#### DELETE /news/{news_id}
- Umumiy:
    - URL orqali yuborilgan id ga ega yangilikni o'chiradi. Muvaffaqiyatli bajarilganida 'True' qiymatini qaytaradi.
- Namuna: `curl -X DELETE http://127.0.0.1:5000/news/5`
```
{
  "success": true
}
```