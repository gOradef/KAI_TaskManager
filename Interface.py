from Vault import Vault

class Interface:
	vault: Vault

	def __init__(self, vault: Vault):
		self.vault = vault

	def changeVault(self):