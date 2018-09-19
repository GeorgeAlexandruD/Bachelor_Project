using BasicChat;
using MVCSolution.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Web;
using MongoDB.Bson;
using MongoDB.Driver;
using System.Threading.Tasks;
using MongoDB.Driver.GeoJsonObjectModel;

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
			Console.WriteLine("new class");

			var user = db.Users.Where(u => u.OBD_Id == id).FirstOrDefault();

			string target = user.UserName;

			Console.WriteLine(id);
			Console.WriteLine(target);

			//ChatHub ch = new ChatHub();
			//ch.Send("love you", target);
		}
		public Parkinglot Location(double lat, double lng)
		{
			

			var client = new MongoClient();
			var mongo_db = client.GetDatabase("GeoDB");
			var collection = mongo_db.GetCollection<Parkinglot>("parkinglot");
														  
			try
            
			{
				       
                var point = GeoJson.Point(GeoJson.Geographic(lat, lng));
				var query = new FilterDefinitionBuilder<Parkinglot>().GeoIntersects(tag => tag.location, point);

				var plots = collection.Find<Parkinglot>(query).FirstOrDefault();
				return plots;
			
			}    
			catch (Exception e){
				Console.WriteLine(e);
			}
			return null;
		}
    }
}

/*db.parkinglot.find({coordinates:
#                  {$geoIntersects:
#                      {$geometry:{ "type" : "Point",
#                           "coordinates" : [57.047748, 9.926616] }
#                       }
#                   }
#              })
*/