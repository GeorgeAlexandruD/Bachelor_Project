using System.Threading.Tasks;
using Microsoft.AspNet.SignalR;
using System.Linq;
using System.Collections.Generic;
using System.Collections.Concurrent;

namespace BasicChat
{
   
    
    public class ChatHub :Hub
    {

        public override Task OnConnected()
        {
            return base.OnConnected();
        }

        public override Task OnDisconnected(bool stopCalled)
        {
            return base.OnDisconnected(stopCalled);
        }

        public static void Send(string message, string to)
        {
            var hubCtx = GlobalHost.ConnectionManager.GetHubContext<ChatHub>();
            hubCtx.Clients.User(to).send(message);

        }

        
    }
   
}