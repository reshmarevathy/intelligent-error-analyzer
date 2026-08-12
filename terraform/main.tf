terraform { required_version=">= 1.6.0" required_providers { null={source="hashicorp/null",version="~> 3.2"} } }
provider "null" {}
resource "null_resource" "project" { provisioner "local-exec" { command="echo Intelligent Error Analyzer IaC" } }
