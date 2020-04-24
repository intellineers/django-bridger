# import requests
# import pandas as pd

# from rest_framework.response import Response
# from bridger.pandas.views import PandasAPIView
# from bridger.pandas import fields as pf
# from bridger import display as dp


# class ClubHouseView(PandasAPIView):
#     filter_backends = []
#     permission_classes = []

#     LIST_ENDPOINT = "bridger:clubhouse"
#     LIST_TITLE = "Pandas List"

#     LIST_DISPLAY = dp.ListDisplay(
#         fields=[
#             dp.Field(key="name", label="Name"),
#             dp.Field(key="story_type", label="Type"),
#         ],
#     )

#     pandas_fields = pf.PandasFields(
#         fields=[
#             pf.PKField(key="id", label="ID"),
#             pf.CharField(key="name", label="Title"),
#             pf.CharField(key="story_type", label="Type"),
#         ]
#     )

#     def get(self, request):
#         self.request = request
#         API_TOKEN = ""
#         response = requests.get(
#             f"https://api.clubhouse.io/api/v3/projects/1045/stories?token={API_TOKEN}",
#             headers={"Content-Type": "application/json"},
#         )
#         df = pd.DataFrame.from_dict(response.json())
#         return Response({"results": df.T.to_dict().values(), "aggregates": {}})

