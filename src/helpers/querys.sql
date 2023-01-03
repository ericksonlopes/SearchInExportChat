select
    phone,
    message,
    date,
    id_file,
    name

from files
         inner join messages im on files.id = im.id_file

where im.id_file = 3
and phone = '@erickson.lds';


select count(message) from messages where id_file = 3 and phone = '@erickson.lds';