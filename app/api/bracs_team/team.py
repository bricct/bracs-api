# @api.route('/post_team', methods=['POST'])
# def post_team():
#   data = json.loads(request.data)
#   name = data['username']
#   image = None
#   if 'image' in data.keys():
#     image = data['image']
#   team = Team(name=name, image=image)

#   try:
#     db_session.add(team)
#     db_session.commit()
#   except:
#     # if team with that name already exists return default response
#     return defaultResponse()

#   return response({"teamID":team.id}, 200)


# @api.route('/team/<int:teamID>', methods=['GET'])
# def get_team(teamID):

#   authUser = processToken(request.headers["Authorization"])

#   # bad token
#   if not authUser:
#     return defaultResponse()

#   # user is not an admin and is not getting themselves
#   if not authUser.isAdmin:
#     return defaultResponse()

#   team = db_session.query(Team).filter_by(id=teamID).one_or_none()

#   if team:
#     return response(team, 200)

#   return response({"error":"user not found"}, 200)
