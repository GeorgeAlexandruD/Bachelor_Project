using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using MVCSolution;
using MVCSolution.Controllers;
using MVCSolution.Models;
using MongoDB.Driver;
using NLog;
using NUnit.Framework;
using System.ServiceModel.Channels;
using MapUsersSample;

namespace UnitTests
{
    [TestClass]
    public class CheckDBTests
    {
        [SetUp]
        public void Setup(ISession session)
        {
           
        }

        [TestMethod]
        public void TestMethod1()
        {
            //Mock<ApplicationDbContext> db = new Mock<ApplicationDbContext>();
            //Mock<MongoClient> mdb = new Mock<MongoClient>();
            //Mock<Logger> log = new Mock<Logger>();

            ApplicationDbContext db = new ApplicationDbContext();
            MongoClient mdb = new MongoClient();
            Logger log = LogManager.GetCurrentClassLogger();

            CheckDB checkdb = new CheckDB(db, mdb, log);
            
         

            
        }
    }
}
