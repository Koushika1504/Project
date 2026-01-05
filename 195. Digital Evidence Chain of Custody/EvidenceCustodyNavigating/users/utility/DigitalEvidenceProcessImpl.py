# views.py

import os
import random
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
from django.shortcuts import render
from django.conf import settings

class DigitalEvidenceProcess:
    PHASES = ["Identification", "Collection", "Preservation", "Examination", "Analysis", "Presentation"]

    def __init__(self, tamper_chance=0.1, fail_chance=0.05):
        self.evidence_log = []
        self.phase_counts = {phase: 0 for phase in self.PHASES}
        self.tampered = []
        self.failed = []
        self.tamper_chance = tamper_chance
        self.fail_chance = fail_chance
        self.evidence_details = {}

    def add_evidence_details(self, evidence_id, evidence_type, description, source):
        self.evidence_details[evidence_id] = {
            'type': evidence_type,
            'description': description,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }

    def process_evidence(self, evidence_id):
        for phase in self.PHASES:
            if random.random() < self.tamper_chance:
                self.tampered.append((evidence_id, phase))
                self.evidence_log.append((evidence_id, phase, 'tampered'))
                break
            if random.random() < self.fail_chance:
                self.failed.append((evidence_id, phase))
                self.evidence_log.append((evidence_id, phase, 'failed'))
                break
            self.evidence_log.append((evidence_id, phase, 'ok'))
            self.phase_counts[phase] += 1

    def simulate_with_details(self, evidence_list):
        for evidence in evidence_list:
            self.add_evidence_details(
                evidence['id'],
                evidence['type'],
                evidence['description'],
                evidence['source']
            )
            self.process_evidence(evidence['id'])

    def plot_phase_counts(self, path):
        phases = list(self.phase_counts.keys())
        counts = [self.phase_counts[phase] for phase in phases]
        plt.figure(figsize=(8, 5))
        plt.bar(phases, counts, color='skyblue')
        plt.title("Evidence Count per Phase")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    def plot_process_flow(self, path):
        G = nx.DiGraph()
        for i in range(len(self.PHASES) - 1):
            G.add_edge(self.PHASES[i], self.PHASES[i + 1])
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, arrowsize=20)
        plt.title("Digital Forensics Process Flow")
        plt.savefig(path)
        plt.close()

    def plot_evidence_types(self, path):
        if not self.evidence_details:
            return
        evidence_types = {}
        for details in self.evidence_details.values():
            ev_type = details['type']
            evidence_types[ev_type] = evidence_types.get(ev_type, 0) + 1
        plt.figure(figsize=(8, 6))
        plt.pie(evidence_types.values(), labels=evidence_types.keys(), autopct='%1.1f%%')
        plt.title("Distribution of Evidence Types")
        plt.savefig(path)
        plt.close()
