# -*- coding: utf-8 -*-

# ########################## Copyrights and license ############################
#                                                                              #
# Copyright 2012 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2012 Zearin <zearin@gonk.net>                                      #
# Copyright 2013 Vincent Jacques <vincent@vincent-jacques.net>                 #
#                                                                              #
# This file is part of PyGithub.                                               #
# http://pygithub.readthedocs.io/                            #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
# ##############################################################################

import Framework

import datetime


class Organization(Framework.TestCase):
    def setUp(self):
        Framework.TestCase.setUp(self)
        self.org = self.g.get_organization("BeaverSoftware")

    def testAttributes(self):
        self.assertEqual(self.org.avatar_url, "https://secure.gravatar.com/avatar/d563e337cac2fdc644e2aaaad1e23266?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-orgs.png")
        self.assertEqual(self.org.billing_email, "BeaverSoftware@vincent-jacques.net")
        self.assertEqual(self.org.blog, None)
        self.assertEqual(self.org.collaborators, 0)
        self.assertEqual(self.org.company, None)
        self.assertEqual(self.org.created_at, datetime.datetime(2012, 2, 9, 19, 20, 12))
        self.assertEqual(self.org.disk_usage, 112)
        self.assertEqual(self.org.email, None)
        self.assertEqual(self.org.followers, 0)
        self.assertEqual(self.org.following, 0)
        self.assertEqual(self.org.gravatar_id, None)
        self.assertEqual(self.org.html_url, "https://github.com/BeaverSoftware")
        self.assertEqual(self.org.id, 1424031)
        self.assertEqual(self.org.location, "Paris, France")
        self.assertEqual(self.org.login, "BeaverSoftware")
        self.assertEqual(self.org.name, None)
        self.assertEqual(self.org.owned_private_repos, 0)
        self.assertEqual(self.org.plan.name, "free")
        self.assertEqual(self.org.plan.private_repos, 0)
        self.assertEqual(self.org.plan.space, 307200)
        self.assertEqual(self.org.private_gists, 0)
        self.assertEqual(self.org.public_gists, 0)
        self.assertEqual(self.org.public_repos, 2)
        self.assertEqual(self.org.total_private_repos, 0)
        self.assertEqual(self.org.type, "Organization")
        self.assertEqual(self.org.url, "https://api.github.com/orgs/BeaverSoftware")

        # test __repr__() based on this attributes
        self.assertEqual(self.org.__repr__(), 'Organization(name=None, id=1424031)')

    def testEditWithoutArguments(self):
        self.org.edit()

    def testEditWithAllArguments(self):
        self.org.edit("BeaverSoftware2@vincent-jacques.net", "http://vincent-jacques.net", "Company edited by PyGithub", "BeaverSoftware2@vincent-jacques.net", "Location edited by PyGithub", "Name edited by PyGithub")
        self.assertEqual(self.org.billing_email, "BeaverSoftware2@vincent-jacques.net")
        self.assertEqual(self.org.blog, "http://vincent-jacques.net")
        self.assertEqual(self.org.company, "Company edited by PyGithub")
        self.assertEqual(self.org.email, "BeaverSoftware2@vincent-jacques.net")
        self.assertEqual(self.org.location, "Location edited by PyGithub")
        self.assertEqual(self.org.name, "Name edited by PyGithub")

    def testEditHookWithMinimalParameters(self):
        hook = self.org.create_hook("web", {"url": "http://foobar.com"})
        hook = self.org.edit_hook(hook.id, "mobile", {"url": "http://barfoo.com"})
        self.assertEqual(hook.name, "mobile")

    def testEditHookWithAllParameters(self):
        hook = self.org.create_hook("web", {"url": "http://foobar.com"}, ["fork"], False)
        hook = self.org.edit_hook(hook.id, "mobile", {"url": "http://barfoo.com"}, ["spoon"], True)
        self.assertEqual(hook.name, "mobile")
        self.assertEqual(hook.events, ["spoon"])
        self.assertEqual(hook.active, True)

    def testCreateTeam(self):
        team = self.org.create_team("Team created by PyGithub")
        self.assertEqual(team.id, 189850)

    def testCreateTeamWithAllArguments(self):
        repo = self.org.get_repo("FatherBeaver")
        team = self.org.create_team("Team also created by PyGithub", [repo], "push")
        self.assertEqual(team.id, 189852)

    def testDeleteHook(self):
        hook = self.org.create_hook("web", {"url": "http://foobar.com"})
        self.org.delete_hook(hook.id)

    def testPublicMembers(self):
        lyloa = self.g.get_user("Lyloa")
        self.assertFalse(self.org.has_in_public_members(lyloa))
        self.org.add_to_public_members(lyloa)
        self.assertTrue(self.org.has_in_public_members(lyloa))
        self.org.remove_from_public_members(lyloa)
        self.assertFalse(self.org.has_in_public_members(lyloa))

    def testGetPublicMembers(self):
        self.assertListKeyEqual(self.org.get_public_members(), lambda u: u.login, ["jacquev6"])

    def testGetHooks(self):
        self.assertListKeyEqual(self.org.get_hooks(), lambda h: h.id, [257993])

    def testGetIssues(self):
        self.assertListKeyEqual(self.org.get_issues(), lambda i: i.id, [])

    def testGetIssuesWithAllArguments(self):
        requestedByUser = self.g.get_user().get_repo("PyGithub").get_label("Requested by user")
        issues = self.org.get_issues("assigned", "closed", [requestedByUser], "comments", "asc", datetime.datetime(2012, 5, 28, 23, 0, 0))
        self.assertListKeyEqual(issues, lambda i: i.id, [])

    def testGetMembers(self):
        self.assertListKeyEqual(self.org.get_members(), lambda u: u.login, ["cjuniet", "jacquev6", "Lyloa"])

    def testMembers(self):
        lyloa = self.g.get_user("Lyloa")
        self.assertTrue(self.org.has_in_members(lyloa))
        self.org.remove_from_members(lyloa)
        self.assertFalse(self.org.has_in_members(lyloa))

    def testGetRepos(self):
        self.assertListKeyEqual(self.org.get_repos(), lambda r: r.name, ["FatherBeaver", "TestPyGithub"])

    def testGetReposWithType(self):
        self.assertListKeyEqual(self.org.get_repos("public"), lambda r: r.name, ["FatherBeaver", "PyGithub"])

    def testGetEvents(self):
        self.assertListKeyEqual(self.org.get_events(), lambda e: e.type, ["CreateEvent", "CreateEvent", "PushEvent", "PushEvent", "DeleteEvent", "DeleteEvent", "PushEvent", "PushEvent", "DeleteEvent", "DeleteEvent", "PushEvent", "PushEvent", "PushEvent", "CreateEvent", "CreateEvent", "CreateEvent", "CreateEvent", "CreateEvent", "PushEvent", "PushEvent", "PushEvent", "PushEvent", "PushEvent", "PushEvent", "ForkEvent", "CreateEvent"])

    def testGetTeams(self):
        self.assertListKeyEqual(self.org.get_teams(), lambda t: t.name, ["Members", "Owners"])

    def testCreateHookWithMinimalParameters(self):
        hook = self.org.create_hook("web", {"url": "http://foobar.com"})
        self.assertEqual(hook.id, 257967)

    def testCreateHookWithAllParameters(self):
        hook = self.org.create_hook("web", {"url": "http://foobar.com"}, ["fork"], False)
        self.assertTrue(hook.active)
        self.assertEqual(hook.id, 257993)

    def testCreateRepoWithMinimalArguments(self):
        repo = self.org.create_repo(name="TestPyGithub")
        self.assertEqual(repo.url, "https://api.github.com/repos/BeaverSoftware/TestPyGithub")

    def testCreateRepoWithAllArguments(self):
        team = self.org.get_team(141496)
        repo = self.org.create_repo(name="TestPyGithub2", description="Repo created by PyGithub", homepage="http://foobar.com",
                                    private=False, has_issues=False, has_wiki=False, has_downloads=False, team_id=team.id)
        self.assertEqual(repo.url, "https://api.github.com/repos/BeaverSoftware/TestPyGithub2")

    def testCreateRepositoryWithAutoInit(self):
        repo = self.org.create_repo(name="TestPyGithub", auto_init=True, gitignore_template="Python")
        self.assertEqual(repo.url, "https://api.github.com/repos/BeaverSoftware/TestPyGithub")

    def testCreateFork(self):
        pygithub = self.g.get_user("jacquev6").get_repo("PyGithub")
        repo = self.org.create_fork(pygithub)
        self.assertEqual(repo.url, "https://api.github.com/repos/BeaverSoftware/PyGithub")
