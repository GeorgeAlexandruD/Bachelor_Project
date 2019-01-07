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
using System.Web.Mvc;
using System.Data.Entity.Validation;
using NLog;

namespace MVCSolution.Controllers
{
    public class CheckDB
    {
       
        private ApplicationDbContext _db;
        private MongoClient _dbm;
        private Logger _log;

        public CheckDB(ApplicationDbContext db, MongoClient dbm, Logger log)
        {
            _dbm = dbm;
            _db = db;
            _log = log;
        }
        public string GetUser(string id)
        {
            var target = _db.Users.Where(u => u.OBD_Id == id).FirstOrDefault();
            return target.UserName;
        }
        public ParkinglotModel Location(double lat, double lng)
        {  
            var mongo_db = _dbm.GetDatabase("GeoDB");
            var collection = mongo_db.GetCollection<ParkinglotModel>("parkinglot");

            try
            {
                var point = GeoJson.Point(GeoJson.Geographic(lat, lng));
                var query = new FilterDefinitionBuilder<ParkinglotModel>().GeoIntersects(tag => tag.location, point);

                var plots = collection.Find<ParkinglotModel>(query).FirstOrDefault();
                return plots;

            }
            catch (Exception e)
            {
                _log.Error(e);
            }
            return null;
        }
        public void AddToDB(string target, DateTime date, int price)
        {
            date = new DateTime(date.Year, date.Month, date.Day, date.Hour, date.Minute, date.Second, date.Kind);
            var user = _db.Users.Where(u => u.UserName == target).FirstOrDefault();
            string uid = user.Id;//[*]
            var did = user.OBD_Id;
            var test = new ParkingOrder
            {
                DeviceId = did,//target.deviceid
                UserId = uid,
                PowerOff = date,
                Price = price
            };
            Debug.WriteLine(test);
            _db.ParkingOrders.Add(test);
            try
            {
                _db.SaveChanges();
            }
            catch (Exception e)
            {
                _log.Error(e);
            }

          
        }
        public double PriceCalculation(string did, DateTime date)
        {
            DateTime? parkDate = null;
            int price;
            double result = -1;
            date = new DateTime(date.Year, date.Month, date.Day, date.Hour, date.Minute, date.Second, date.Kind);
            var parkOrder = _db.ParkingOrders.FirstOrDefault(b => b.DeviceId ==did  && b.PowerOn==null );//[*]"2GQ-16010084"

            if (parkOrder != null )
            {
                parkDate = parkOrder.PowerOff;
                price = parkOrder.Price;

                parkOrder.PowerOn = date;
                _db.SaveChanges();

                if (parkDate != null )
                {
                    TimeSpan span = date.Subtract((DateTime)parkDate);

                    if (span.TotalMinutes < 5)
                        result = 0;
                    else
                        result = span.TotalHours * price;
                }
            }
            return result;
            
        }
    }
}