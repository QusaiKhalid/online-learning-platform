package authz

# Default deny all requests
default allow = false

# Allow admins to perform any action
allow if {
    input.user.roles[_] == "admin"
}

# Allow teachers and students to read their own user details
allow if {
    input.user.roles[_] == "teacher"
    input.action == "read"
    input.resource.type == "user"
    input.resource.id == input.user.id
}

allow if {
    input.user.roles[_] == "student"
    input.action == "read"
    input.resource.type == "user"
    input.resource.id == input.user.id
}

# Allow teachers and students to update their own user details
allow if {
    input.user.roles[_] == "teacher"
    input.action == "update"
    input.resource.type == "user"
    input.resource.id == input.user.id
}

allow if {
    input.user.roles[_] == "student"
    input.action == "update"
    input.resource.type == "user"
    input.resource.id == input.user.id
}

# Allow admins to fetch all users
allow if {
    input.user.roles[_] == "admin"
    input.action == "read"
    input.resource.type == "user"
    input.resource.id == "*"
}

# Allow admins to create users
allow if {
    input.user.roles[_] == "admin"
    input.action == "create"
    input.resource.type == "user"
}

# Allow admins to delete users
allow if {
    input.user.roles[_] == "admin"
    input.action == "delete"
    input.resource.type == "user"
}
