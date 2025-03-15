package authz

# Default deny all requests
default allow = false

# Allow admins to perform any action within their organization
allow if {
    input.user.roles[_] == "admin"
    input.resource.organization_id == input.user.organization_id
}

# Allow teachers and students to read their own user details within their organization
allow if {
    input.user.roles[_] == "teacher"
    input.action == "read"
    input.resource.type == "user"
    input.resource.id == input.user.id
    input.resource.organization_id == input.user.organization_id
}

allow if {
    input.user.roles[_] == "student"
    input.action == "read"
    input.resource.type == "user"
    input.resource.id == input.user.id
    input.resource.organization_id == input.user.organization_id
}

# Allow teachers and students to update their own user details within their organization
allow if {
    input.user.roles[_] == "teacher"
    input.action == "update"
    input.resource.type == "user"
    input.resource.id == input.user.id
    input.resource.organization_id == input.user.organization_id
}

allow if {
    input.user.roles[_] == "student"
    input.action == "update"
    input.resource.type == "user"
    input.resource.id == input.user.id
    input.resource.organization_id == input.user.organization_id
}

# Allow admins to fetch all users within their organization
allow if {
    input.user.roles[_] == "admin"
    input.action == "read"
    input.resource.type == "user"
    input.resource.organization_id == input.user.organization_id
}

# Allow admins to create users within their organization
allow if {
    input.user.roles[_] == "admin"
    input.action == "create"
    input.resource.type == "user"
    input.resource.organization_id == input.user.organization_id
}

# Allow admins to delete users within their organization
allow if {
    input.user.roles[_] == "admin"
    input.action == "delete"
    input.resource.type == "user"
    input.resource.organization_id == input.user.organization_id
}