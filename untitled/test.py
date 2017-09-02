class VMname:
    def createVM(self, name):
        # Remember Self just refers to the object you are passing firstHot or secondHost
        self.name = name
        # Initialize the argument we passed with the object

    def stateVM(self):
        print(self.name)


# Create your first object
firstHost = VMname()
firstHost.createVM('email.foo.org')
Hname1 = firstHost.stateVM()
print( 'You named your VM ', str(Hname1))

# Create your second object
secondHost = VMname()
secondHost.createVM('ldap.bar.org')
Hname2 = secondHost.stateVM()
print('You named your VM', str(Hname2))

# Notice what gets printed when we call the method stateVM, it prints &#039;None&quot;
# If we replace print(self.name) with return(self.name)
# it will pass the attribute back outside of the class.
# Next we call a method directly using the variable assigned to the object and class &quot;firstHost&quot; with a &quot;.statVM() calling the method.
# It will not pass back data from the class without us using return.
# Notice it says none.

print(firstHost.stateVM())
print(Hname2)