using EasyNetQ;
using EasyNetQ.Topology;
using Microsoft.Owin;
using Owin;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using MVCSolution.Controllers;
using Newtonsoft.Json.Linq;
using Microsoft.AspNet.SignalR;
using System.Net;
using Microsoft.Owin.Security.Cookies;
using Microsoft.AspNet.Identity;
using System.Diagnostics;
using MVCSolution.Models;
using System;
using MongoDB.Driver;
using NLog;
[assembly: OwinStartupAttribute(typeof(MVCSolution.Startup))]
namespace MVCSolution
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            //GlobalHost.DependencyResolver.Register(typeof(IUserIdProvider), () => new MyIdProvider());

            app.UseCookieAuthentication(new CookieAuthenticationOptions
            {
                AuthenticationType = DefaultAuthenticationTypes.ApplicationCookie,
                LoginPath = new PathString("/Home/Index")
            });

            app.MapSignalR();
           
            ConfigureAuth(app);
            Listener();
        }

        public interface IUserIdProvider
        {
            string GetUserId(IRequest request);
        }
        private void Listener()
        {
            var logger = LogManager.GetCurrentClassLogger();
            ApplicationDbContext db = new ApplicationDbContext();
            MongoClient mdb = new MongoClient();
            CheckDB cdb = new CheckDB(db, mdb, logger);
           
            try
            {

                var bus = RabbitHutch.CreateBus("host=localhost").Advanced;

                var queue = bus.QueueDeclare("data_queue");
                var exchange = bus.ExchangeDeclare("data", ExchangeType.Topic, false, false, false, false, null, false);
                var binding = bus.Bind(exchange, queue, "#");

                bus.Consume(queue, (body, properties, info) => Task.Factory.StartNew(() =>

                  {
                      string message = Encoding.UTF8.GetString(body);
                      dynamic json = JObject.Parse(message);
                      PacketHandler pd = new PacketHandler(cdb);
                      
                      if (json.packet_type == "alarm")
                          pd.Alarm(json);
                  }));

            }
            catch(Exception e)
            {
                logger.Error(e);
            }
           
        }       
    }
}
