import unittest

from crenz.dns_tester import is_ip, DnsTester
import dns.name
import dns.rdatatype
import dns.rrset
import dns.exception
import copy


class TestDnsCheck(unittest.TestCase):
  def setUp(self):
    self.dt = DnsTester('a12-65.akam.net.')
    self.dt.load_file('myexample.zone')
 
  def test_load_file1(self):
    dt1=DnsTester('a12-65.akam.net.')
    dt1.load_file('myexample.zone')
    self.assertEqual( dt1.zonename, 'myexample.com')

  def test_load_file2(self):
    with self.assertRaises(dns.exception.SyntaxError):
      dt1=DnsTester('a12-65.akam.net.')
      dt1.load_file('myexample_broken.zone')

  def test_load_txt1(self):
    with open('myexample.zone') as f:
      zonetxt = f.read()
      dt1 = DnsTester('a12-65.akam.net.')
      dt1.load_txt(zonetxt)
      self.assertEqual( dt1.zonename, 'myexample.com')

  def test_load_txt2(self):
    with self.assertRaises(dns.exception.SyntaxError):
      with open('myexample_broken.zone') as f:
        zonetxt = f.read()
        dt1 = DnsTester('a12-65.akam.net.')
        dt1.load_txt(zonetxt)
  
  def test_init_resolver1(self):
    dt1 = DnsTester('a.root-servers.net.')
    dt1.init_resolver()
    self.assertEqual( dt1.authns, 'a.root-servers.net.')
    self.assertEqual( dt1.resolver.nameservers[0], '198.41.0.4')

  def test_init_resolver2(self):
    dt1 = DnsTester('8.8.8.8')
    dt1.init_resolver()
    self.assertEqual( dt1.authns, '8.8.8.8')
    self.assertEqual( dt1.resolver.nameservers[0], '8.8.8.8')


  def test_get_query_answer1(self):
    name, rdtype, rdataset = self.dt.get_rdataset_from_zone('www', 'A')
    ret = self.dt.get_query_answer(name, rdtype)
    self.assertEqual( type(ret), dns.rrset.RRset )

   #def test_query_check(self):
   # name, rdtype, rdataset = self.dt.get_rdataset_from_zone('www', 'A')
   # ret = self.dt.query_check(name, rdataset)
   # print(ret)

  def test_get_rdata_from_zone1(self):
    ret = self.dt.get_rdataset_from_zone('www', 'A')
    self.assertEqual( ret[0].to_text(), 'www')
    self.assertEqual( dns.rdatatype.to_text( ret[1] ), 'A'  )
    self.assertIsNotNone(ret[2])

  def test_get_rdata_from_zone2(self):
    ret = self.dt.get_rdataset_from_zone('www123', 'NS')
    self.assertEqual( ret[0].to_text(), 'www123')
    self.assertEqual( dns.rdatatype.to_text( ret[1] ), 'NS'  )
    self.assertIsNone(ret[2])

  #def test_zone_check(self):
  #  ret = self.dt.zone_check()
  #  print(ret)
  
  def test_is_ip1(self):
    self.assertTrue( is_ip('1.2.3.4') )
 
  def test_is_ip2(self):
    self.assertTrue( is_ip('fe80::980f:62ff:fe74:203') )

  def test_is_ip3(self):
    self.assertFalse( is_ip('myexample.com') )




if __name__ == '__main__':
  unittest.main()

