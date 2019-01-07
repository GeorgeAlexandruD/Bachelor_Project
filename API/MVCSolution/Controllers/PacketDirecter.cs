using MVCSolution.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver;
using System.Diagnostics;

namespace MVCSolution.Controllers
{
    public class PacketHandler
    {

        private CheckDB _cdb;

        public PacketHandler(CheckDB cdb)
        {
            _cdb = cdb;
        }



        public void Alarm(dynamic json)
        {
            string id = json.unit_id;
            DateTime timestamp = json.timestamp;
            string socketMsg = "";
            string username = "";

            if (json.power_off == true)
            {      
                //double lat = json.gps.lat;
                //double lng = json.gps.lng;
                double lat = 57.047748;
                double lng = 9.926616;

                username = _cdb.GetUser(id);
               
                var location = _cdb.Location(lat, lng);

                
                if (location != null)
                {
                    _cdb.AddToDB(username, timestamp, location.price);
                    socketMsg = "You have parked in " + location.name + ".\n" +
                                "Price per hour is " + location.price;

                    BasicChat.ChatHub.Send(socketMsg, username);
                }
            }
            if(json.power_on == true)
            {
                try
                {
                    username = _cdb.GetUser(id);
                    
                    double result = _cdb.PriceCalculation(id, timestamp);
                    if (result >= 0)
                        socketMsg = "You have to pay: " + result;
                    else
                        socketMsg = "Something went terribly wrong.";

                    BasicChat.ChatHub.Send(socketMsg, username);
                }
                catch(Exception e)
                {
                    Debug.WriteLine(e);
                }
            }

        }

    }
}