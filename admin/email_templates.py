## confrimation email html version
confirmation_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <h4 class='m-4 text-center'>Thank you {name} for your purchase</h4>
</body>
</html>'''

## confimation email plain text version
confirmation_text = 'Thank you {name} for your purchase'

## 
confirmation_admin = '{fname} {lname} booked {booking} spaces for {event}'

cancellation_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <h4 class='m-4 text-center'>We are sorry, but {event} on {date} at {time} was cancelled</h4>
</body>
</html>'''

cancellation_text = 'We are sorry, but {event} on {date} at {time} was cancelled'

remider_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <h4 class='m-4 text-center'>Please remember that {event} is happening tomorrow({date}). - Please arrive 30 minutes before, because doors are closed at {time}</h4>
</body>
</html>'''

reminder_txt = 'Please remember that {event} is happening tomorrow({date} - Please arrive 30 minutes before, because doors are closed at {time})'

admin_reminder = '{event} is due tomorrow({date}) at {time}. Please log in to your website to close booking'