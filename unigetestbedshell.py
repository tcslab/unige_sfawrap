import time
import mysql.connector
import requests
import json

from sfa.util.sfalogging import logger

class unigetestbedShell():

	def __init__(self, nodes, slices, indexes):
		self.nodes = nodes
		self.slices = slices
		self.indexes = indexes

	def nodeExists(self,nodeId, nodes):
		for node in nodes:
			if node.get("node_id") == nodeId.get("node_id"):
				return True 


		return False

        def FilterList(myfilter, mylist):
			result = []
			result.extend(mylist)
			for item in mylist:
				 for key in myfilter.keys():
					 if 'ids' in key:
						 pass
					 else:
						 if myfilter[key] != item[key]:
							 result.remove(item)
							 break
			return result

        def GetTestbedInfo(self):
                return {'name': 'unigetestbed', 'latitude': 46.1763879, 'longitude': 61.399586, 'domain':'129.194.70.52:8111/ero2proxy'}

        def GetNodes(self,filter={}):
                nodes_list = []
                response = requests.get('http://129.194.70.52:8111/ero2proxy/service')
                data = response.json()
                nodes = data["services"]

                for idx, val in enumerate(nodes):
                                for i in range(0,len(val["resources"])):
                        		resource = val["resources"][i]
                			node = {'hostname': resource["hostname"],
		                                # 'ip': resource["ip"],
		                                'ip': resource["uri"].replace("\\",""),
		                                'port': resource["port"],
		                                'type': resource["type"],
		                                'protocol': resource["protocol"],
		                                'uri': resource["uri"].replace("\\",""),
		                                'hardware': resource["hardware"],
		                                'node_id': resource["node_id"],
		                                'resources': [{'name': resource["resourcesnode"]["name"],
		                                    'path': resource["resourcesnode"]["path"],
		                                    'unit': resource["resourcesnode"]["unit"],
		                                    'data_type': resource["resourcesnode"]["data_type"],
		                                    'type': resource["resourcesnode"]["type"]}]}
                        		nodes_list.append(node)
		result = []
		result.extend(nodes_list)
		if 'node_ids' in filter:
			for node in nodes_list:				
				if node['node_id'] not in filter['node_ids']:
					result.remove(node)
				
                return result

        def GetSlices(self,filter={}):
		logger.info("GETSlices")
		logger.info(filter)
		result = []
		result.extend(self.slices)
		if 'slice_name' in filter:
			for slice in self.slices:
				if slice['slice_name'] not in filter['slice_name']:
					result.remove(slice)
		
                return self.slices


        def GetUsers(filter={}):
                result = []
                return result


        #def GetKeys():



        #add

        def AddNode(self,node):
                return True

        def AddSlice(self,slice):
			logger.info("AddSlice")
			logger.info(slice)
			if not isinstance(slice, dict):
				return False
			for key in slice.keys():
				if key not in['slice_name','user_ids','node_ids','enabled','expired']:
					return False

			slice['slice_id'] = self.indexes['slices_index']
			slice['expires'] = int(time.time())+60*60*24*30
			self.indexes['slices_index']+=1
			self.slices.append(slice)

			logger.info(self.slices)
			return slice['slice_id']


        def AddUser(self,user):
                return []


        def AddUserKey(self,param):
                return True

        def AddUserToSlice(self,param):
			logger.info("Add user to slice")
			logger.info(param)
			if not isinstance(param, dict):
				return False
			try:
				for slice in self.slices:
					 if param['slice_id'] == slice['slice_id']:
						 if not 'user_ids' in slice: slice['user_ids'] = []
						 slice['user_ids'].append(param['user_id'])
						 return True
				return False
			except:
				return False		

        def AddSliceToNodes(self,param):
			logger.info("AddSliceToNode")
			logger.info(param)
			if not isinstance(param, dict):
				return False
			try:
				for slice in self.slices:
					 if param['slice_id'] == slice['slice_id']:
						 if not 'node_ids' in slice: slice['node_ids'] = []
						 slice['node_ids'].extend(param['node_ids'])
						 return True
				return False
			except:
				return False

        #Delete

        def DeleteNode(self,param):
                return True



        def DeleteSlice(self,param):
		print(param)
                return True



        def DeleteUser(self,param):
                return True



        def DeleteKey(self,param):
                return True

        def DeleteUserFromSlice(self,param):
                return True



        def DeleteSliceFromNodes(self,param):
			if not isinstance(param, dict):
				return False
			try:
				for slice in self.slices:
					 if param['slice_id'] == slice['slice_id']:
					 	for node_id in param['node_ids']:
							if node_id in slice['node_ids']:
								slice['node_ids'].remove(node_id)
						return True
				return False
			except:
				return False


        #Update

        def UpdateNode(self,param):
                return True



        def UpdateSlice(self,param):
                return True



        def UpdateUser(self,param):
                return True
