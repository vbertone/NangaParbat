//
// Author: Valerio Bertone: valerio.bertone@cern.ch
//

#include "NangaParbat/convolutiontable.h"

#include <iostream>

namespace NangaParbat
{
  //_________________________________________________________________________________
  ConvolutionTable::ConvolutionTable(YAML::Node const& table)
  {
    // Name
    _name  = table["name"].as<std::string>();

    // C.M.E.
    _Vs  = table["CME"].as<double>();

    // qT bin bounds
    _qTv = table["qT_bounds"].as<std::vector<double>>();

    // Ogata unscaled coordinates
    _z   = table["Ogata_coordinates"].as<std::vector<double>>();

    // Q grid
    _Qg  = table["Qgrid"].as<std::vector<double>>();

    // xi grid
    _xig = table["xigrid"].as<std::vector<double>>();

    for (auto const& qT : _qTv)
      _W.insert({qT, table[qT].as<std::vector<std::vector<std::vector<double>>>>()});
  }

  //_________________________________________________________________________________
  ConvolutionTable::ConvolutionTable(std::string const& infile):
    ConvolutionTable(YAML::LoadFile(infile))
  {
  }

  //_________________________________________________________________________________
  std::map<double,double> ConvolutionTable::Convolute(std::function<double(double const&, double const&, double const&)> const& fNP) const
  {
    std::map<double,double> pred;
    for (auto const& qT : _qTv)
      {
	double cs = 0;
	for (int n = 0; n < (int) _z.size(); n++)
	  {
	    const double b = _z[n] / qT;
	    for (int tau = 0; tau < (int) _Qg.size(); tau++)
	      {
		const double Q    = _Qg[tau];
		const double zeta = Q * Q;
		const double Vtau = Q / _Vs;
		for (int alpha = 0; alpha < (int) _xig.size(); alpha++)
		  {
		    const double xi = _xig[tau];
		    cs += _W.at(qT)[n][tau][alpha] * fNP(Vtau * xi, b, zeta) * fNP(Vtau / xi, b, zeta);
		  }
	      }
	  }
	pred.insert({qT, cs});
      }
    return pred;
  }
}