using System.Threading.Tasks;
using Microsoft.AspNet.SignalR;
using System.Linq;
using System.Collections.Generic;
using System.Collections.Concurrent;

namespace BasicChat
{
   
    public class User
    {

        public string Name { get; set; }
        public HashSet<string> ConnectionIds { get; set; }
    }
    public class ChatHub :Hub
    {
        private static readonly ConcurrentDictionary<string, User> Users
       = new ConcurrentDictionary<string, User>();

        public override Task OnConnected()
        {

            string userName = Context.User.Identity.Name;
            string connectionId = Context.ConnectionId;

            var user = Users.GetOrAdd(userName, _ => new User
            {
                Name = userName,
                ConnectionIds = new HashSet<string>()
            });

            lock (user.ConnectionIds)
            {

                user.ConnectionIds.Add(connectionId);

                // TODO: Broadcast the connected user
            }
            Clients.AllExcept(user.ConnectionIds.ToArray()).userConnected(userName);
            return base.OnConnected();
        }

        public override Task OnDisconnected(bool stopCalled)
        {

            string userName = Context.User.Identity.Name;
            string connectionId = Context.ConnectionId;

            User user;
            Users.TryGetValue(userName, out user);

            if (user != null)
            {

                lock (user.ConnectionIds)
                {

                    user.ConnectionIds.RemoveWhere(cid => cid.Equals(connectionId));

                    if (!user.ConnectionIds.Any())
                    {

                        User removedUser;
                        Users.TryRemove(userName, out removedUser);

                        // You might want to only broadcast this info if this 
                        // is the last connection of the user and the user actual is 
                        // now disconnected from all connections.
                        Clients.Others.userDisconnected(userName);
                    }
                }
            }

            return base.OnDisconnected(stopCalled);
        }

        public void Send(string message, string to)
        {
            Clients.User(to).received(to, message);


            //User receiver;
            //if (Users.TryGetValue(to, out receiver))
            //{

            //    User sender = GetUser(Context.User.Identity.Name);

            //    IEnumerable<string> allReceivers;
            //    lock (receiver.ConnectionIds)
            //    {
            //        lock (sender.ConnectionIds)
            //        {

            //            allReceivers = receiver.ConnectionIds.Concat(
            //                sender.ConnectionIds);
            //        }
            //    }

            //    foreach (var cid in allReceivers)
            //    {

            //        Clients.Client(cid).received(
                    
            //             sender.Name,
            //            message

            //        );
            //    }
            //}
        }

        private User GetUser(string username)
        {

            User user;
            Users.TryGetValue(username, out user);

            return user;
        }
    }
   
}