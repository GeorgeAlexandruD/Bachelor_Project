using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver.GeoJsonObjectModel;

namespace MVCSolution.Models
{
    public class ParkinglotModel
    {
        public ObjectId Id { get; set; }
        public GeoJsonObject<GeoJson2DCoordinates> location { get; set; }
        public string name { get; set; }
        public int price { get; set; }


    }
}