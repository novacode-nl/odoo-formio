# Changelog

## 16.0.2.1

Improve public user check, by checking either:
- no user in request.env, or ...
- the request user has the public user group (the added check).
This change isn't solving a vulnerability, but a public GET request was too restrictive and could be denied too quickly.

## 16.0.2.0

Fix security vulnerability for GET (file) request.\
The form access-check was missing here, which determines whether the (file) request is allowed or forbidden.\
Even though those file requests are obscured by a UUID (unique randomized) string in the file name, those were still publicly accessible before this fix.

## 16.0.1.0

Release.
