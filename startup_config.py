#some startup configuration, design and config manually
startupconfig = {
    "common_intpolicy" : "Common_AccessPortPolicyGroup",
    "untag_intpolicy" : "physical_machine_port",
    "tenant1" : "BEJ1",
    "appprofile1" : "BEJ_AppProfile"
}

subnet_get_epgvlan = {
    "172.31.54.0/25":"BackupAndNFS_EPG,541",
    "172.31.54.128/25":"ExadataClient_BD,542",
    "172.31.55.0/24":"Replication_EPG,55",
    "172.31.43.128/25":"BareMetal_EPG,43"
}