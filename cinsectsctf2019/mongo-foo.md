# mongo-foo

mongo-foo was a tiny cli key-value store written in python, backed by a mongodb.
It offered the commands `encrypt`, `decrypt`, `store` and `retrieve`, where `decrypt` was broken and only `store` and `retrieve` were being used.

After a successflly `store`, you received an id, which you could supply in `retrieve`.

There were no vulnerabilities in the service, only the mongodb was not binding to localhost only. Many teams did not notice, because the vulnbox had an unintended mongodb which was listening on 127.0.0.1 only:

Since the host file of the vulnbox had two entries for localhost, one being 127.0.0.1, the other one being a different machine, the service used the mongodb on the different server for some teams.

Exploiting this vulnerability was trivial - dump the database, decode the flag, submit.

Fixing this vulnerability was trivial - restrict connections to the mongodb.
