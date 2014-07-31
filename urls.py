import webapp2
import views

urls = [  (r'/check_user', views.CheckUser), (r'/get', views.Get_Events), (r'/post_event', views.Add_Event) ]

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '223030033',
}

app = webapp2.WSGIApplication(urls, debug=True, config=config)

