export PYTHONPATH=$(pwd)
flask --app rest/server run -p 4080
http :4080/register_session
http ':4080/<session_id>/edge?left=33&right=39'
http ':4080/e2e98f33-1ec4-41b6-92eb-49a0568df93a/update?left=1&right=2&dissent=123&respect=3'
http POST ':4080/24acdeb1-5f82-4caa-8da6-0b4aeff16789/update' left=1 right=2 dissent=123 respect=1