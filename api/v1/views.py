
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.v1.serializers import InterviewSerializer
from interviewapp.models import Interview, Interviewer, Candidate


class InterviewViewSet(viewsets.ModelViewSet):
    model = Interview
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()

    @staticmethod
    def if_candidate(candidate_email, slot=None, pk=None):
        if Interview.objects.filter(slot=slot, candidate__email=candidate_email):
            return '', 'Candidate already has an interview at given time slot.'

        try:
            candidate, _ = Candidate.objects.get_or_create(email=candidate_email)

            if pk:
                interview = Interview.objects.get(id=pk)
                interview.candidate = candidate
                interview.save()

                if interview.candidate and interview.interviewer:
                    interview.is_scheduled = True
                    interview.save()

            else:
                interview, _ = Interview.objects.get_or_create(slot=slot, candidate=candidate)

            return InterviewSerializer(interview).data, ''

        except Exception as e:
            return '', str(e)

    @staticmethod
    def if_interviewer(interviewer_email, slot=None, pk=None):
        interviewer_emails = interviewer_email.split(',')
        if slot:
            if Interview.objects.filter(slot=slot, interviewer__email__in=interviewer_emails):
                return '', 'Interviewer/s already has an interview at given time slot.'

        interviewer_list = []
        try:
            for interviewer_email in interviewer_emails:
                obj, _ = Interviewer.objects.get_or_create(email=interviewer_email)
                interviewer_list.append(obj)

            if pk:
                interview = Interview.objects.get(id=pk)
                interview.interviewer.set(interviewer_list)

                if interview.candidate and interview.interviewer:
                    interview.is_scheduled = True
                    interview.save()

            else:
                interview = Interview.objects.create(slot=slot)
                interview.interviewer.set(interviewer_list)

            return InterviewSerializer(interview).data, ''

        except Exception as e:
            return '', str(e)

    def create(self, request, *args, **kwargs):
        interviewer_email = request.data.get('interviewer_email')
        candidate_email = request.data.get('candidate_email')
        slot = request.data.get('slot')

        if not slot:
            return Response({'detail': 'Slot information is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if interviewer_email:
            interview, error = self.if_interviewer(interviewer_email, slot)
            if error:
                return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
            return Response(interview, status=status.HTTP_200_OK)

        if candidate_email:
            interview, error = self.if_candidate(candidate_email, slot)
            if error:
                return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
            return Response(interview, status=status.HTTP_200_OK)

        return Response({'detail': 'Interview could not created'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        interviewer_email = request.data.get('interviewer_email')
        candidate_email = request.data.get('candidate_email')

        if interviewer_email:
            interview, error = self.if_interviewer(interviewer_email, pk=kwargs.get('pk'))
            if error:
                return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
            return Response(interview, status=status.HTTP_200_OK)

        if candidate_email:
            interview, error = self.if_candidate(candidate_email, pk=kwargs.get('pk'))
            if error:
                return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
