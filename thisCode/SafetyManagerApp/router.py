# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from django.urls import path
from django.conf.urls import url
# from api.tf2.view import tf2Api
from api.tf2.views import tf2View
from api.logs.views import LogsView,LogDetailView
from api.accesstokens.views import AccessTokenView
from api.equipments.views import EquipmentsView
from api.channels.views import ChannelView
from api.ppeselection import views as PPESelectViews
from api.ppeselection.views import PPESelectView
from api.details  import views as detailsview
from api.slack  import views as slackview
from api.detection  import views as detectionview
from api.accesstokens  import views as AccessTokenMethods
from api.dbsettings  import views as dbsettingsview

urlpatterns = [
    path('equipments/', EquipmentsView.as_view()),
    path('equipments/<int:pk>', EquipmentsView.as_view()),

    path('logs/', LogsView.as_view()),
    path('logs/<int:pk>', LogDetailView.as_view()),
    path('tf2/', tf2View.as_view()),
    

    path('equipments/', EquipmentsView.as_view()),
    path('equipments/<int:pk>', EquipmentsView.as_view()),

    path('access_token/', AccessTokenView.as_view()),
    path('access_token/<int:pk>', AccessTokenView.as_view()),
    path('access_token/getValidAccessToken', AccessTokenMethods.getValidAccessToken ),

    
    path('channels/', ChannelView.as_view()),
    path('channels/<int:pk>', ChannelView.as_view()),
    
    path('ppeselections/getselection/', PPESelectViews.get_selection),
    path('ppeselections/', PPESelectView.as_view()), 
    path('ppeselections/<int:pk>', PPESelectView.as_view()), 
    
    path('slack/send_message/', slackview.send_message), 
      
    path('detection/advanceObjectDetection/', detectionview.advance_image_detection), 
    path('detection/objectDetection/', detectionview.image_detection), 

    path('dbsettings/db_export/', dbsettingsview.db_export),  
    path('dbsettings/db_import/', dbsettingsview.db_import),
    path('details/total_violation/', detailsview.total_violation), 
    path('details/total_logs/', detailsview.total_logs),
    # url(r'^tf2$',tf2Api),
    # url(r'^tf2/([0-9]+)$',tf2Api), 
    


     
]

