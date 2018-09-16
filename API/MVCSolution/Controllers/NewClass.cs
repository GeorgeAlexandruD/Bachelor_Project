using BasicChat;
using MVCSolution.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Web;

namespace MVCSolution.Controllers
{
    public class NewClass
    {
        
        private ApplicationDbContext db = new ApplicationDbContext();

        public NewClass()
        {
           
        }
        public void FunctionThatSolvesThings(string id)
        {

            var user = db.Users.Where(u => u.OBD_Id == id).FirstOrDefault();
            
            string target = user.UserName;

            Debug.WriteLine(id);
            Debug.WriteLine(target);

            //ChatHub ch = new ChatHub();
            //ch.Send("love you", target);
        }
    
    }
}