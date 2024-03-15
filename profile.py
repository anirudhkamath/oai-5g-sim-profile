#!/usr/bin/python

tourDescription = """
### Running 5G simulation on POWDER and OpenAirInterface5G

This profile is derived from a tutorial session created by Dustin Maas for MERIF 2023.
It deploys a single compute node with an image that includes docker,
docker-compose, tshark, oai-cn5g-fed v1.4.0, and docker images for all of the
OAI 5G core network functions. It also includes source code and a prebuilt
version of the OAI RAN stack (gNB, nrUE, RF simulator). It shows how
profiles like this one can be used in the classroom to explore 5G networks.

The description and instructions for the original MERIF session can be found
[here](https://gitlab.flux.utah.edu/powderrenewpublic/merif2023/-/blob/main/content/teaching-5g-oai.md).
"""

tourInstructions = """

Note: After you instantiate an experiment, you have to wait until the POWDER
portal shows your experiment status in green as "Your experiment is ready"
before proceeding.


"""


import geni.portal as portal
import geni.rspec.pg as rspec
import geni.urn as URN
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.rspec.emulab as emulab

request = portal.context.makeRequestRSpec()

node = request.RawPC( "node" )
node.hardware_type = "d430"
node.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"  # disk image on POWDER.
node.startVNC()

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

portal.context.printRequestRSpec()
