
<!DOCTYPE html>
<html>
    <head>
        <title>폼</title>
        <meta charset="UTF-8">
        <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin: auto;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="email"],
        input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
    </head>
    <body>
        <form method="post" enctype="multipart/form-data">
            <label for="name">이름:</label>
            <input type="text" id="name" name="name" required autocomplete="off">

            <label for="phone">연락처:</label>
            <input type="text" id="phone" name="phone" required autocomplete="off">

            <label for="email">이메일:</label>
            <input type="email" id="email" name="email" required autocomplete="off">

            <label for="attach">파일첨부:</label>
            <input type="file" id="attach" name="attach">

            <button type="submit">등록</button>
        </form>
    </body>
    
</html>
<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    $attach = $_POST['attach'];

    echo "name is $name<br/>";
    echo "phone is $phone<br/>";
    echo "email is $email<br/>";
    echo "attach is $attach<br/>";
}
?>