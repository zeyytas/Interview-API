from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

from api.v1.serializers import InterviewSerializer
from interviewapp.models import Interviewer, Interview, Candidate


class InterviewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interview-list')

    def test_create_interviewer(self):
        email = 'interviewer@gmail.com'
        self.client.post(self.url, {'interviewer_email': email, 'slot': 11}, format='json')

        try:
            Interviewer.objects.get(email=email)
        except ObjectDoesNotExist:
            self.fail('Creation of Interview object failed.')

        emails = 'interviewer2@gmail.com,interviewer3@gmail.com'
        self.client.post(self.url, {'interviewer_email': emails, 'slot': 11}, format='json')

        try:
            Interviewer.objects.filter(email__in=['interviewer@gmail.com', 'interviewer2@gmail.com'])
        except ObjectDoesNotExist:
            self.fail('Creation of Interview objects failed.')

    def test_create_candidate(self):
        email = 'candidate@gmail.com'

        self.client.post(self.url, {'candidate_email': email, 'slot': 15}, format='json')
        try:
            Candidate.objects.get(email=email)
        except ObjectDoesNotExist:
            self.fail('Creation of Candidate object failed.')

    def test_create_interview_by_interviewers(self):

        email = 'interviewer4@gmail.com,interviewer5@gmail.com'
        emails = email.split(',')

        response = self.client.post(self.url, {'interviewer_email': email, 'slot': 13}, format='json')

        try:
            interviewers = Interviewer.objects.filter(email__in=emails)
            interview = Interview.objects.filter(interviewer__in=interviewers).distinct().get()
            import ipdb;ipdb.set_trace()
            serialized_obj = InterviewSerializer(interview)

            self.assertDictEqual(response.data, serialized_obj.data)

        except ObjectDoesNotExist:
            self.fail('Creation of Interview object failed.')

    def test_create_interview_by_candidate(self):

        email = 'candidate2@gmail.com'
        slot = 17
        response = self.client.post(self.url, {'candidate_email': email, 'slot': slot}, format='json')

        candidate = Candidate.objects.get(email=email)

        interview = Interview.objects.get(slot=slot, candidate=candidate)
        serialized_obj = InterviewSerializer(interview).data

        self.assertDictEqual(response.data, serialized_obj)

    def test_update_interview_by_interviewer(self):
        candidate = Candidate.objects.create(email='candidate3@gmail.com')
        interview = Interview.objects.create(slot=18, candidate=candidate)

        email = 'interviewer6@gmail.com'
        self.client.put(reverse('interview-detail', args=[interview.id]), {'interviewer_email': email}, format='json')

        interviewer = Interviewer.objects.get(email=email)
        interview = Interview.objects.get(id=interview.id)

        self.assertEqual(interview.is_scheduled, True)
        self.assertEqual(interviewer, interview.interviewer.get())

    def test_update_interview_by_candidate(self):
        interviewer = Interviewer.objects.create(email='interviewer7@gmail.com')
        interview = Interview.objects.create(slot=15)
        interview.interviewer.set([interviewer])
        interview_id = interview.id

        email = 'candidate4@gmail.com'
        self.client.put(reverse('interview-detail', args=[interview_id]), {'candidate_email': email}, format='json')

        try:
            candidate = Candidate.objects.get(email=email)
            interview = Interview.objects.get(id=interview_id)

            self.assertEqual(interview.is_scheduled, True)
            self.assertEqual(candidate, interview.candidate)

        except ObjectDoesNotExist:
            self.fail('Update of Interview object failed.')

    def test_get_interview_by_candidate(self):

        candidate_emails = ['candidate5@gmail.com', 'candidate6@gmail.com', 'candidate7@gmail.com']
        candidate = Candidate.objects.create(email=candidate_emails[0])
        candidate2 = Candidate.objects.create(email=candidate_emails[1])
        candidate3 = Candidate.objects.create(email=candidate_emails[2])

        interviewer = Interviewer.objects.create(email='interviewer7@gmail.com')
        interviewer2 = Interviewer.objects.create(email='interviewer8@gmail.com')

        interview = Interview.objects.create(slot=11, candidate=candidate, is_scheduled=True)
        interview.interviewer.set([interviewer, interviewer2])

        interview = Interview.objects.create(slot=12, candidate=candidate3, is_scheduled=True)
        interview.interviewer.set([interviewer])

        interview = Interview.objects.create(slot=14, candidate=candidate2, is_scheduled=True)
        interview.interviewer.set([interviewer2])

        for candidate_email in candidate_emails:
            response = self.client.get(self.url, {'candidate_email': candidate_email}, format='json')
            serialized_obj = InterviewSerializer(Interview.objects.filter(candidate__email=candidate_email), many=True)

            self.assertEqual(response.data['results'], serialized_obj.data)

    def test_get_interview_by_interviewer(self):
        interviewer_emails = ['interviewer9@gmail.com', 'interviewer10@gmail.com']

        interviewer = Interviewer.objects.create(email=interviewer_emails[0])
        interviewer2 = Interviewer.objects.create(email=interviewer_emails[1])

        candidate = Candidate.objects.create(email='candidate8@gmail.com')
        candidate2 = Candidate.objects.create(email='candidate9@gmail.com')

        interview = Interview.objects.create(slot=10, candidate=candidate, is_scheduled=True)
        interview.interviewer.set([interviewer, interviewer2])

        interview = Interview.objects.create(slot=17, candidate=candidate2, is_scheduled=True)
        interview.interviewer.set([interviewer2])

        for interviewer_email in interviewer_emails:
            response = self.client.get(self.url, {'interviewer_email': interviewer_email}, format='json')
            serialized_obj = InterviewSerializer(Interview.objects.filter(interviewer__email=interviewer_email),
                                                 many=True)

            self.assertEqual(response.data['results'], serialized_obj.data)

        response = self.client.get(self.url,
                                   {'interviewer_email': '{},{}'.format(interviewer_emails[0],
                                                                        interviewer_emails[1])}, format='json')

        serialized_obj = InterviewSerializer(Interview.objects.filter(interviewer__email__in=interviewer_emails),
                                             many=True)

        self.assertEqual(response.data['results'], serialized_obj.data)

    def test_get_interview_by_interviewer_and_candidate(self):
        interviewer_emails = ['interviewer11@gmail.com', 'interviewer12@gmail.com']
        candidate_emails = ['candidate10@gmail.com', 'candidate11@gmail.com', 'candidate12@gmail.com']

        interviewer = Interviewer.objects.create(email=interviewer_emails[0])
        interviewer2 = Interviewer.objects.create(email=interviewer_emails[1])

        candidate = Candidate.objects.create(email=candidate_emails[0])
        candidate2 = Candidate.objects.create(email=candidate_emails[1])
        candidate3 = Candidate.objects.create(email=candidate_emails[2])

        interview = Interview.objects.create(slot=10, candidate=candidate, is_scheduled=True)
        interview.interviewer.set([interviewer, interviewer2])

        interview = Interview.objects.create(slot=17, candidate=candidate2, is_scheduled=True)
        interview.interviewer.set([interviewer2])

        interview = Interview.objects.create(slot=18, candidate=candidate3, is_scheduled=True)
        interview.interviewer.set([interviewer2])

        response = self.client.get(self.url, {'interviewer_email': interviewer_emails[1],
                                              'candidate_email': candidate_emails[1]}, format='json')
        serialized_obj = InterviewSerializer(Interview.objects.filter(interviewer__email=interviewer_emails[1],
                                                                      candidate__email=candidate_emails[1]),
                                             many=True)

        self.assertEqual(response.data['results'], serialized_obj.data)