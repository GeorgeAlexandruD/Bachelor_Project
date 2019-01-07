using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace MVCSolution.Controllers
{
    public class ParkingController : Controller
    {
        // GET: Parking
        public ActionResult Index()
        {
            return View();
        }
    }
}