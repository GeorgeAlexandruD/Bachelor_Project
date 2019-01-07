using Microsoft.AspNet.Identity.EntityFramework;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace MVCSolution.Models
{
    
    public class ParkingOrder
    {
        [Key, Column(Order = 0)]
        public string DeviceId { get; set; }
        [Key, Column(Order = 1)]
        public string UserId { get; set; }
        [Key, Column(Order = 2)]
        public DateTime PowerOff { get; set; }
        public DateTime? PowerOn { get; set; }
        public int Price { get; set; }
        public bool? Payed { get; set; }

        [ForeignKey("UserId")]
        public virtual ApplicationUser ApplicationUser { get; set; }
        //public virtual IdentityUser IdentityUser { get; set; }
    }
}