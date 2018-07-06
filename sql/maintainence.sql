/*
every command in this file should be run daily.
I'll probably write a script to do that later but
since this is a pet project, never to be deployed
this falls low on the prioritys list
*/

//delete old login cookies
delete from logged_in_users where (expires<now());
