import subprocess

#print(" Creating EC2...")
#subprocess.run(["ansible-playbook", "create_ec2.yml"], check=True)
==========================================================================
print(" Deleting EC2...")
subprocess.run(["ansible-playbook", "delete_ec2_test.yml"], check=True)
=========================================================================
#print("  Updating Check Point firewall policy...")
#subprocess.run(["ansible-playbook", "-i", "inventory", "add_rule1.yml"], check=True)
=========================================================================
#print("  Deleting Check Point firewall policy...")
#subprocess.run(["ansible-playbook", "-i", "inventory", "delete_rule.yml"], check=True)

print("✅  Done!")